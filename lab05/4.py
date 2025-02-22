import re

def match_string(s):
    pattern = r'^[A-Z][a-z]+$'  
    if re.fullmatch(pattern, s):
        return True
    return False

strings = ["Hello", "KBTU", "hello", "Nazerke", "PpCode", "A", "Abc", "abc"]
for s in strings:
    print(f"'{s}': {match_string(s)}")
