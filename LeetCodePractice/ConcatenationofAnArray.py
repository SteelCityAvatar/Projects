from typing import List

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        
        for i in range(0,len(nums)):
            print(i)
            nums.append(nums[i])
        return nums
a = Solution()
a.getConcatenation(nums)