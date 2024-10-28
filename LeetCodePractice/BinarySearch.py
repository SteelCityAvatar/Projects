from typing import List
class Solution:
    def search(self, nums: List[int],target:int) -> int:
        start = 0
        end = len(nums) - 1
        found = False
        while start <= end and not found:
            if target == nums[start]:
                out = nums.index(nums[start])
                found = True
            else:
                start += 1
                out = -1
        return out