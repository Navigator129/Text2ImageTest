# select nodes from object categories
# construct a tree with the nodes
import json
import random

from tqdm import tqdm
from generatePrompt import *


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
    with open('./files/attribute_datasets.json', 'r') as f:
        objects = json.load(f)
    return objects

def select_relation():
    #select relation nodes
    randidx = 4 # used to select a random relation type
    types = list(relation.keys())
    relation_type = types[random.randint(0, randidx-1)]
    relation_idx = random.randint(0, randidx-1)
    select_relation = relation[relation_type][relation_idx] #randomly select a relation node
    return select_relation

def select_object():
    objects = get_object()
    obj = list(objects.keys())
    obj_idx = random.randint(0, len(obj)-1)
    obj = obj[obj_idx]
    return obj

def select_attribute(obj):
    objects = get_object()
    attr = objects[obj]
    attr_idx = random.randint(0, len(attr)-1)
    attr = attr[attr_idx]
    return attr

def select_color():
    color = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'brown', 'purple', 'pink', 'orange']
    attr_idx = random.randint(0, len(color)-1)
    color = color[attr_idx]
    return color
    

def select_number(relation_node, flag):
    number = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    attr_idx = random.randint(0, len(number)-1)
    number = number[attr_idx]
    #Flag is used to determine if the input node is the second object node in the vertical relation, we don't want see 'one apple is on top of two table'
    if flag:
        if relation_node in relation['top'] or relation_node in relation['bottom']:
            return 'one'
    
    return number

def constructPPT():
    relation_node = select_relation()
    #select object nodes
    obj1 = select_object()
    obj2 = select_object()
    if obj1 == obj2:
        obj2 = select_object()
    #select attribute nodes
    attr1 = select_attribute(obj1)
    attr2 = select_attribute(obj2)

    #select color nodes
    color1 = select_color()
    color2 = select_color()
    #select number nodes
    number1 = select_number(relation_node, False)
    number2 = select_number(relation_node, True)

    #construct the tree
    root = PPT(relation_node)
    root.add_child(PPT(obj1))
    root.add_child(PPT(obj2))
    child1 = root.get_children()[0]
    child2 = root.get_children()[1]
    child1.add_child(PPT(attr1))
    child1.add_child(PPT(color1))
    child1.add_child(PPT(number1))

    child2.add_child(PPT(attr2))
    child2.add_child(PPT(color2))
    child2.add_child(PPT(number2))

    return root 

def mutator(input_PPT):
    mutation = random.randint(1, 5)
    mutate_tree = []
    for i in range(mutation):
        mutator = random.randint(1, 3)

        if mutator == 1:
            new_PPT = add_relation(input_PPT)
            mutate_tree.append(new_PPT)
        elif mutator == 2:
            new_PPT = swap_object(input_PPT)
            mutate_tree.append(new_PPT)
        elif mutator == 3:
            new_PPT = add_attribute(input_PPT)
            mutate_tree.append(new_PPT)
    return mutate_tree

def add_relation(input_PPT):
    #combine two tree
    relation_node = select_relation()
    root = PPT(relation_node)
    old_children = input_PPT.get_children()
    #randomly select one of the children as obj1
    rand_idx = random.randint(0, 1)

    obj1 = old_children[rand_idx].value
    obj2 = select_object()
    if obj1 == obj2:
        obj2 = select_object()
    root.add_child(input_PPT.get_children()[rand_idx])
    root.add_child(PPT(obj2))
    child2 = root.get_children()[1]
    attr = select_attribute(obj2)
    color = select_color()
    number = select_number(relation_node, False)
    child2.add_child(PPT(attr))
    child2.add_child(PPT(color))
    child2.add_child(PPT(number))
    return root

def get_opposite_relation(relation_node):
    if relation_node in relation['top']:
        return 'bottom'
    elif relation_node in relation['bottom']:
        return 'top'
    elif relation_node in relation['left']:
        return 'right'
    elif relation_node in relation['right']:
        return 'left'

def swap_object(input_PPT):
    #swap the object and the relation nodes
    original_relation = input_PPT.value
    obj1 = input_PPT.get_children()[0]
    obj2 = input_PPT.get_children()[1]
    new_relation_type = get_opposite_relation(original_relation)
    new_relation = relation[new_relation_type][random.randint(0, 3)]

    root = PPT(new_relation)
    obj1_attr = obj1.get_children()
    obj2_attr = obj2.get_children()
    root.add_child(PPT(obj2.value))
    root.add_child(PPT(obj1.value))
    child1 = root.get_children()[0]
    child2 = root.get_children()[1]
    for attr in obj2_attr:
        child1.add_child(attr)
    for attr in obj1_attr:
        child2.add_child(attr)

    return root



def add_attribute(input_PPT):
    #add an attribute to a node
    relation_node = input_PPT.value
    obj1 = input_PPT.get_children()[0]
    obj2 = input_PPT.get_children()[1]
    obj1_value = obj1.value
    obj2_value = obj2.value
    new_attr1 = select_attribute(obj1.value)
    new_attr2 = select_attribute(obj2.value)
    attr1 = obj1.get_children()
    attr2 = obj2.get_children()
    attr1_values = get_attribute_values(attr1)
    attr2_values = get_attribute_values(attr2)
    #construct the new tree which is the same as the input tree
    root = PPT(relation_node)
    root.add_child(PPT(obj1_value))
    root.add_child(PPT(obj2_value))
    for attr in attr1_values:
        root.get_children()[0].add_child(PPT(attr))
    for attr in attr2_values:
        root.get_children()[1].add_child(PPT(attr))

    #add new attribute to the tree
    if len(attr1_values) == 8:
        pass
    else:
        if new_attr1 not in attr1_values:
            root.get_children()[0].add_child(PPT(new_attr1))
        else:
            new_attr1 = select_attribute(obj1.value)
            while new_attr1 in attr1_values:
                new_attr1 = select_attribute(obj1.value)
            root.get_children()[0].add_child(PPT(new_attr1))

    if len(attr2) == 8:
        pass
    else:
        if new_attr2 not in attr2_values:
            root.get_children()[1].add_child(PPT(new_attr1))
        else:
            new_attr2 = select_attribute(obj2.value)
            while new_attr2 in attr2_values:
                new_attr2 = select_attribute(obj2.value)
            root.get_children()[1].add_child(PPT(new_attr1))
    return root


if __name__ == "__main__":
    ppt_list = []
    for i in tqdm(range(1000)):
        ppt = constructPPT()
        ppt_list.append(ppt)
        mutate_tree = mutator(ppt)
        ppt_list = ppt_list + mutate_tree
    
    i = 0
    for ppt in tqdm(ppt_list):
        generatePrompt(ppt, i)
        i += 1
    
    print("Done!")
    

    
