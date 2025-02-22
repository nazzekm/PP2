import re

text = "hello_world_how_are_you"
pattern = r"_([a-z])"

def repl(match):
    return match.group(1).upper()

result = re.sub(pattern, repl, text)
print(result)