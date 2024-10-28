#my solution
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        right = 1
        while right < len(nums)+1:
            if nums[right-1]!=val:
                nums[k]=nums[right-1]
                k+=1
                right +=1
            else:
                right +=1
        return k
# [0,1,2,2,3,0,4,2]
# val = 2
#neetode solution
# class Solution:
#     def removeElement(self, nums: List[int], val: int) -> int:
#         k = 0
#         # right = 1
#         for i in range(len(nums)):
#             if nums[i]!=val:
#                 nums[k]=nums[i]
#                 k+=1
        
#         return k, nums

# a = Solution()
# a.removeElement([0,1,2,2,3,0,4,2], 2)
        