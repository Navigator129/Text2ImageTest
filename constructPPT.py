import random
import json
import time


relation = {"top": ['on top of', 'above', 'Atop', 'Upon'], "bottom": ["Beneath", "Under", "Below", "Underneath"], 
            "left": ["To the left of","On the left side of", "Leftward of", "Adjacent to the left of"], 
            "right": ["To the right of", "On the right side of", "Rightward of", "Adjacent to the right of"]}



class PPT:
    def __init__(self, value):
        self.value = value
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    
    def remove_child(self, child):
        self.children.remove(child)

    def get_children(self):
        return self.children
    
    def traverse(self):
        print(self.value)
        for child in self.children:
            child.traverse()

def get_object():
    with open('./files/object_datasets.json', 'r') as f:
        objects = json.load(f)
    return objects

def get_attribute():
    with open('./files/attribute_datasets.json', 'r') as f:
        attribute = json.load(f)
    return attribute

def select_relation():
    #select relation nodes
    randidx = 4 # used to select a random relation type
    types = list(relation.keys())
    relation_type = types[random.randint(0, randidx-1)]
    relation_idx = random.randint(0, randidx-1)
    select_relation = relation[relation_type][relation_idx] #randomly select a relation node
    return select_relation

def get_relate_category(category):
    if category == 'velicle':
        related_category = 'outdoor'
    if category == 'outdodr':
        related_category = 'velicle'
    if category == "food":
        related_category = "kitchen"
    if category == "kitchen":
        related_category = "food"
    if category == "accessory":
        related_category = "furniture"
    if category == "electronic":
        related_category = "furniture"
    if category == "appliance":
        related_category = "furniture"
    if category == "indoor":
        related_category = "furniture"
    if category == "furniture":
        related_category = "indoor"
    return related_category
    

def select_object():
    objects = get_attribute()
    obj_list = list(objects.keys())
    timestamp = float(time.time())
    random.seed(timestamp)
    obj_idx = random.randint(0, len(obj_list)-1)
    obj = obj_list[obj_idx]
    return obj

def select_related_object(obj):
    obj_dict = get_object()
    for key, value in obj_dict.items():
        if obj in value:
            obj_type = key
            break
    if obj_type:
        related_category = get_relate_category(obj_type)
        related_obj_list = get_object()[related_category]
        rand_idx = random.randint(0, len(related_obj_list)-1)
        related_obj = related_obj_list[rand_idx]
        return related_obj
    else:
        return None

def select_attribute(obj):
    objects = get_attribute()
    attr = objects[obj]
    attr_idx = random.randint(0, len(attr)-1)
    attr = attr[attr_idx]
    return attr

def select_color():
    color = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'brown', 'purple', 'pink']
    attr_idx = random.randint(0, len(color)-1)
    color = color[attr_idx]
    return color
    

def select_number():
    # number = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'] 
    # attr_idx = random.randint(0, len(number)-1)
    # number = number[attr_idx]
    # #Flag is used to determine if the input node is the second object node in the vertical relation, we don't want see 'one apple is on top of two table'
    # if flag:
    #     if relation_node in relation['top'] or relation_node in relation['bottom']:
    #         return 'one'
    
    # return number
    return 'one'

def obj_node_contruction(obj_node, attr, color, number):
    obj_node.add_child(PPT(attr))
    obj_node.add_child(PPT(color))
    obj_node.add_child(PPT(number))


def construction(M_check, relation_node, obj1, obj2, attr1, attr2, color1, color2, number1, number2):
    #M_check: boolean to check if multiple relation nodes are used
    #construct the tree
    root = PPT(M_check)
    relation = PPT(relation_node)
    root.add_child(relation)
    child1 = PPT(obj1)
    child2 = PPT(obj2)
    relation.add_child(child1)
    relation.add_child(child2)
    attr1 = select_attribute(obj1)
    attr2 = select_attribute(obj2)
    color1 = select_color()
    color2 = select_color()
    number1 = select_number()
    number2 = select_number()
    obj_node_contruction(child1, attr1, color1, number1)
    obj_node_contruction(child2, attr2, color2, number2)

    return root 


def constructUnrelatedPPT():
    #construct a default tree
    relation_node = select_relation()
    #select object nodes
    obj1 = select_object()
    obj2 = select_object()
    #select attribute nodes
    attr1 = select_attribute(obj1)
    attr2 = select_attribute(obj2)

    #select color nodes
    color1 = select_color()
    color2 = select_color()
    #select number nodes
    number1 = select_number()
    number2 = select_number()
    root = construction(False, relation_node, obj1, obj2, attr1, attr2, color1, color2, number1, number2)
    return root

def constructRelatedPPT():
    #construct a related tree
    relation_node = select_relation()
    #select object nodes
    obj1 = select_object()
    obj2 = select_related_object(obj1)
    #select attribute nodes
    attr1 = select_attribute(obj1)
    attr2 = select_attribute(obj2)

    #select color nodes
    color1 = select_color()
    color2 = select_color()
    #select number nodes
    number1 = select_number()
    number2 = select_number()
    root = construction(False, relation_node, obj1, obj2, attr1, attr2, color1, color2, number1, number2)
    return root