class Solution:
    def isValid(self, s: str) -> bool:
        lookup = {'(':')','{':'}','[':']','(':')'}
        stack = []
        for i in s:
            if i in lookup:
                stack.append(i)
            elif not stack or lookup[stack.pop()]!=i:
                return False
        return not stack


        c