import json

error_detect_file = ''
origin_file = ''

with open(error_detect_file, 'r') as f:
    error_detect = json.load(f)

with open(origin_file, 'r') as f:
    origin = json.load(f)

for err_dict in error_detect:
    for key in err_dict:
        for PPT_info in origin:
            PPT_info['idx'] = int(key)
            origin.remove(PPT_info)


for i in range(len(origin)):
    origin[i]['idx'] = i

with open(origin_file, 'w') as f:
    json.dump(origin, f, indent=4)
