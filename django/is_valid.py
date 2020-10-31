def is_valid(self, raise_exception=False):
    assert not hasattr(self, 'restore_object'), (
        'Serializer `%s.%s` has old-style version 2 `.restore_object()` '
        'that is no longer compatible with REST framework 3. '
        'Use the new-style `.create()` and `.update()` methods instead.' %
        (self.__class__.__module__, self.__class__.__name__)
    )

    assert hasattr(self, 'initial_data'), (
        'Cannot call `.is_valid()` as no `data=` keyword argument was '
        'passed when instantiating the serializer instance.'
    )

    if not hasattr(self, '_validated_data'):
        try:
            # self.initial_data 为传入的data，是个字典
            self._validated_data = self.run_validation(self.initial_data)
        except ValidationError as exc:
            self._validated_data = {}
            self._errors = exc.detail
        else:
            self._errors = {}

    if self._errors and raise_exception:
        raise ValidationError(self.errors)

    return not bool(self._errors)

def run_validation(self, data=empty):
    """
    We override the default `run_validation`, because the validation
    performed by validators and the `.validate()` method should
    be coerced into an error dictionary with a 'non_fields_error' key.
    """
    # 验证空值
    (is_empty_value, data) = self.validate_empty_values(data)
    if is_empty_value:
        return data

    value = self.to_internal_value(data)
    try:
        self.run_validators(value)
        value = self.validate(value)
        assert value is not None, '.validate() should return the validated data'
    except (ValidationError, DjangoValidationError) as exc:
        raise ValidationError(detail=as_serializer_error(exc))

    return value

def validate_empty_values(self, data):
    """
    Validate empty values, and either:

    * Raise `ValidationError`, indicating invalid data.
    * Raise `SkipField`, indicating that the field should be ignored.
    * Return (True, data), indicating an empty value that should be
      returned without any further validation being applied.
    * Return (False, data), indicating a non-empty value, that should
      have validation applied as normal.
    """
    # self.read_only默认空值，serializers类返回False
    if self.read_only:
        return (True, self.get_default())

    if data is empty:
        if getattr(self.root, 'partial', False):
            raise SkipField()
        if self.required:
            self.fail('required')
        return (True, self.get_default())

    if data is None:
        if not self.allow_null:
            self.fail('null')
        return (True, None)

    return (False, data)

def to_internal_value(self, data):
    """
    Dict of native values <- Dict of primitive datatypes.
    """
    # data为dict
    if not isinstance(data, Mapping):
        message = self.error_messages['invalid'].format(
            datatype=type(data).__name__
        )
        raise ValidationError({
            api_settings.NON_FIELD_ERRORS_KEY: [message]
        }, code='invalid')

    # OrderedDict 对加入的键值顺序进行排序，两个简直不一样依旧不相等
    ret = OrderedDict()
    errors = OrderedDict()
    fields = self._writable_fields

    for field in fields:
        validate_method = getattr(self, 'validate_' + field.field_name, None)
        primitive_value = field.get_value(data)
        try:
            validated_value = field.run_validation(primitive_value)
            if validate_method is not None:
                validated_value = validate_method(validated_value)
        except ValidationError as exc:
            errors[field.field_name] = exc.detail
        except DjangoValidationError as exc:
            errors[field.field_name] = get_error_detail(exc)
        except SkipField:
            pass
        else:
            set_value(ret, field.source_attrs, validated_value)

    if errors:
        raise ValidationError(errors)

    return ret

def _writable_fields(self):
    return [
        field for field in self.fields.values() if not field.read_only
    ]

def fields(self):
    """
    A dictionary of {field_name: field_instance}.
    """
    # `fields` is evaluated lazily. We do this to ensure that we don't
    # have issues importing modules that use ModelSerializers as fields,
    # even if Django's app-loading stage has not yet run.
    if not hasattr(self, '_fields'):
        self._fields = BindingDict(self)
        for key, value in self.get_fields().items():
            self._fields[key] = value
    return self._fields


class BindingDict(collections.MutableMapping):
    """
    This dict-like object is used to store fields on a serializer.

    This ensures that whenever fields are added to the serializer we call
    `field.bind()` so that the `field_name` and `parent` attributes
    can be set correctly.
    """

    def __init__(self, serializer):
        self.serializer = serializer
        self.fields = OrderedDict()

    def __setitem__(self, key, field):
        self.fields[key] = field
        field.bind(field_name=key, parent=self.serializer)

    def __getitem__(self, key):
        return self.fields[key]

    def __delitem__(self, key):
        del self.fields[key]

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        return dict.__repr__(self.fields)

def get_fields(self):
    """
    Returns a dictionary of {field_name: field_instance}.
    """
    # Every new serializer is created with a clone of the field instances.
    # This allows users to dynamically modify the fields on a serializer
    # instance without affecting every other serializer instance.
    return copy.deepcopy(self._declared_fields)


class SerializerMetaclass(type):
    """
    This metaclass sets a dictionary named `_declared_fields` on the class.

    Any instances of `Field` included as attributes on either the class
    or on any of its superclasses will be include in the
    `_declared_fields` dictionary.
    添加类中字段父类为Field的属性
    并把父类的字段全部加上
    存放于_declared_fields字段
    """

    @classmethod
    def _get_declared_fields(cls, bases, attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]
        fields.sort(key=lambda x: x[1]._creation_counter)

        # If this class is subclassing another Serializer, add that Serializer's
        # fields.  Note that we loop over the bases in *reverse*. This is necessary
        # in order to maintain the correct order of fields.
        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields = [
                    (field_name, obj) for field_name, obj
                    in base._declared_fields.items()
                    if field_name not in attrs
                ] + fields

        return OrderedDict(fields)