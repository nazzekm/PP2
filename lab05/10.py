import re

text = "HelloWorldHowAreYou"
pattern = r"([A-Z])"

def repl(match):
    return "_" + match.group(1).lower()

result = re.sub(pattern, repl, text).strip("_")
print(result)