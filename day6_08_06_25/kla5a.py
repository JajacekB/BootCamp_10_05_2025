class LongestKeyDict(dict):
    def longest_key(self):
        longest = None
        for key in self:
            if longest is None or len(key) > len(longest):
                longest = key
        return longest


art = LongestKeyDict()
art['tomasz'] = 12
art['abraham'] = 7
art['zen'] = 17
print(art.longest_key())

# assert 'abraham' == art.longest_key()
# assert 'zen' == art.longest_key()

class LongestKeyDictMax(dict):
    def longest_key(self):
        return max(self.keys(), key=len)


art = LongestKeyDictMax()
art['tomasz'] = 12
art['abraham'] = 7
art['zen'] = 17
print(art.longest_key())
