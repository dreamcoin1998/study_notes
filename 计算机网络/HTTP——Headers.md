[toc]

# Content-Disposition

此字段指示响应回复的的内容改以何种形式展示，是内联到页面中还是以附件的形式下载并保存。

### 语法

**作为消息主体中的消息头**

可选参数主要有三个：

```
Content-Disposition: inline
Content-Disposition: attachment
Content-Disposition: attachment; filename="filename.jpg"
```

- inline：默认值，表示回复中的消息体会以页面的形式展示
- attachment：表示消息体用该被下载到本地
- filename：当选中attachment时，再指定filename的值将值预先填为下载后的文件名。

**在multipart/form-data类型的应答消息体中**

```
Content-Disposition: form-data
Content-Disposition: form-data; name="fieldName"
Content-Disposition: form-data; name="fieldName"; filename="filename.jpg"
```

第一参数总是固定不变的```form-data```；附加的参数不区分大小写，拥有参数值，参数名和参数值用=连接，参数值用“”括起来，参数之间用逗号分隔；

- name：代表表单字段名的字符串，每个字段会对应一个子部份。如果参数name的值为```_charset_```意味着这个字段表示的不是一个HTML字段，而是在未明确指定字符集的情况下各部分使用默认字符集。

- filename：要传送的文件的初始名称字符串。可选。路径信息必须舍掉，同时进行一定转换以符合服务器文件系统规则，当与```Content-Disposition: attachment```一起使用，被用作“保存”为对话框中呈现给用户的默认文件名。
- filename*：与filename区别在于，采用了 *RFC 5987* 中规定的编码方式。当与filename同时出现，应该采用filename











