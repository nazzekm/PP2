import re

text = "HelloWorldHowAreYou"
result = re.findall(r'[A-Z][^A-Z]*', text)
print(result)