[toc]

# 1. 寻找数组中重复的数字

### 时间优先

用字典以空间换时间

```python
class Solution:
    def findRepeatNumber(self, nums: List[int]) -> int:
        # 时间优先
        # record = dict()
        # for n in nums:
        #     resp = record.get(n, None)
        #     if resp is None:
        #         record[n] = 1
        #     else:
        #         return n
```

### 空间优先

