import chardet

# pip install chardet
# !pip install chardet - w notebook jupyter
# pip - menadżer pakietów python
with open("test.log", "r") as file:
    lines = file.read()
print(lines)

file_path = "test.log"
with open(file_path, 'rb') as file:
    raw_data = file.read()

print(raw_data)

result = chardet.detect(raw_data)
print(result)
print(type(result))

encoding = result["encoding"]
confidence = result["confidence"]
print(encoding)
print(confidence *100)

print(raw_data.decode(encoding=encoding))