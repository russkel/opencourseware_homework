# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.

def expand(text, l, r):
    while l >= 0 and r <= len(text)-1 and text[l] == text[r]:
        l -= 1
        r += 1
        
    return (l+1,r)

def slice_len(tup):
    return tup[1] - tup[0]

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if len(text) == 0:
        return (0,0)
    
    text = text.upper()
    
    longest = (0,1)
    for i in range(len(text)):
        longest = max(expand(text, i, i), expand(text, i, i+1), longest,
                     key=slice_len)    
    return longest

def palindrome(text):
    return text == text[::-1]
    
def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()