
text1 = "علي"
text2 = "علی"

print("Text 1:", text1)
print("Text 2:", text2)

print("Are they equal?", text1 == text2)

for char in text1:
    print(char, ord(char))

print("---------------")

for char in text2:
    print(char, ord(char))
