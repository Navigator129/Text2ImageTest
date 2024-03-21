import json

with open('files/instances_val2017.json', 'r') as load_f:
    data = json.load(load_f)
coco_dataset = data["categories"]
my_dataset = {}
for object in coco_dataset:
    if object['supercategory'] in my_dataset:
        my_dataset[object['supercategory']].append(object['name'])
    else:
        temp = {"{0}".format(object['supercategory']):[object['name']]}
        my_dataset.update(temp)
with open("files/new_cocodataset.json","w") as f:
    json.dump(my_dataset,f)
print(my_dataset)

