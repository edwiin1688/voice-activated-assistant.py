from opencc import OpenCC
cc = OpenCC('s2t')
text = "你会说繁体中文吗"
print(f"Original: {text}")
print(f"Traditional: {cc.convert(text)}")
