import re

text = "HelloWorldHowAreYou"
pattern = r"([A-Z])"
result = re.sub(pattern, r" \1", text).strip()
print(result)