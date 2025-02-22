import re

def check(s):
    pattern = r"a[a-z]+b$"
    if re.search(pattern, s):
        return True
    else:
        return False

test_strings = ["ab", "acb", "abbb", "a123b"]

for s in test_strings:
    print(f"'{s}': {check(s)}")