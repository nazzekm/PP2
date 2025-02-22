import re

def match_string(s):
    pattern = r'^[a-z]+_[a-z]+$'  
    if re.fullmatch(pattern, s):
        return True
    return False

strings = ["hello_world", "Moldakhan_Nazerke", "helloWorld", "pp2_spring","kbtu_site", "_test", "test_"]
for s in strings:
    print(f"'{s}': {match_string(s)}")
