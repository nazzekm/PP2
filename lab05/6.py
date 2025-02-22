import re

text_to_match = "John's email is john.doe@example.com Hello John"

pattern = r"[ ,.]"
result = re.sub(pattern, ":" ,text_to_match) 
print(result)