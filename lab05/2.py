import re

def match_string(s):
    pattern = r"ab{2,3}"
    if re.search(pattern, s):
        return True
    else:
        return False

test_strings = ["a", "aabbbb", "abb", "sabbb", "b", "ba", "abbc"]

for s in test_strings:
    print(f"'{s}': {match_string(s)}")