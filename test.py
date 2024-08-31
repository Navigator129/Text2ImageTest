dict_ = {"1": 'abc', "2": 'def', "3": 'ghi', "141": 'asda'}

for key in dict_:
    print(key)

print(list(dict_.keys()))

if "141" in list(dict_.keys()):
    print('yes')