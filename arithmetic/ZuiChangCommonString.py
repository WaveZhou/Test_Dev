class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if strs is None or len(strs) == 0:
            return ''
        prefix = strs[0]
        for s in strs:
            while s.find(prefix) != 0:
                prefix = prefix[:-1]
        return prefix


if __name__ == "__main__":
    s = Solution()
    print(s.longestCommonPrefix(['asgeg', 'asbgeg', 'asbbrw']))
