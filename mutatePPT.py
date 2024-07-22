# select nodes from object categories
# construct a tree with the nodes
import random
import time

from tqdm import tqdm
from generatePrompt import get_attribute_values
from constructPPT import *


def mutator(input_PPT, related):
    timestamp1 = float(time.time())
    random.seed(timestamp1)
    mutation = random.randint(1, 4)
    mutate_tree = []

    for i in range(mutation):
        timestamp2 = float(time.time())
        random.seed(timestamp2)
        mutator = random.randint(1, 4)
        # mutator = 4

        if mutator == 1:
            new_PPT = change_obj(input_PPT, related)
            mutate_tree.append(new_PPT)
        elif mutator == 2:
            new_PPT = swap_object(input_PPT)
            mutate_tree.append(new_PPT)
        elif mutator == 3:
            new_PPT = add_attribute(input_PPT)
            if new_PPT == input_PPT:
                continue
            mutate_tree.append(new_PPT)
        elif mutator == 4:
            new_PPT = add_relation(input_PPT, related)
            mutate_tree.append(new_PPT)

    return mutate_tree

def duplicate_subtree(input_PPT):
    obj = input_PPT.value
    attr = input_PPT.get_children()
    root = PPT(obj)
    for a in attr:
        new_a = PPT(a.value)
        root.add_child(new_a)
    return root

def change_obj(input_PPT, related):
    #check if the input tree has multiple relation nodes
    M_check = input_PPT.value
    if M_check:
        relation_nodes = input_PPT.get_children()
        new_relation_nodes = []
        for relation_node in relation_nodes:
            old_children = relation_node.get_children()
            #randomly select one of the children as obj1
            rand_idx = random.randint(0, 1)
            old_child = old_children[rand_idx]
            old_child = duplicate_subtree(old_child)
            #construct the new obj node
            if related:
                new_child_value = select_related_object(old_child.value)
            else:
                new_child_value = select_object()
            new_child = PPT(new_child_value)
            new_attr = select_attribute(new_child_value)
            new_color = select_color()
            new_number = select_number()
            obj_node_contruction(new_child, new_attr, new_color, new_number)
            #construct the new tree
            new_relation_node = PPT(relation_node.value)
            new_relation_node.add_child(old_child)
            new_relation_node.add_child(PPT(new_child))
            new_relation_nodes.append(new_relation_node)
        root = PPT(True)
        for relation_node in new_relation_nodes:
            root.add_child(relation_node)
        return root
    else:
        root = PPT(False)
        relation_node = input_PPT.get_children()[0]
        old_children = relation_node.get_children()
        rand_idx = random.randint(0, 1)
        old_child = old_children[rand_idx]
        old_child = duplicate_subtree(old_child)
        #construct the new obj node
        if related:
            new_child_value = select_related_object(old_child.value)
        else:
            new_child_value = select_object()
        new_child = PPT(new_child_value)
        new_attr = select_attribute(new_child_value)
        new_color = select_color()
        new_number = select_number()
        obj_node_contruction(new_child, new_attr, new_color, new_number)
        #construct the new subtree
        new_relation_node = PPT(relation_node.value)
        new_relation_node.add_child(old_child)
        new_relation_node.add_child(new_child)
        root.add_child(new_relation_node)
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
    M_check = input_PPT.value
    if M_check:
        relation_nodes = input_PPT.get_children()
        new_relation_nodes = []
        for relation_node in relation_nodes:
            #get two object nodes
            obj1 = relation_node.get_children()[0]
            obj2 = relation_node.get_children()[1]
            #get the opposite relation value
            op_relation_type = get_opposite_relation(relation_node.value)
            op_relation = relation[op_relation_type][random.randint(0, 3)]
            #construct new subtree
            new_relation_node = PPT(op_relation)
            new_relation_node.add_child(obj2)
            new_relation_node.add_child(obj1)
            new_relation_nodes.append(new_relation_node)
        root = PPT(True)
        for relation_node in new_relation_nodes:
            root.add_child(relation_node)
        return root

    else:
        original_relation_node = input_PPT.get_children()[0]
        original_relation = original_relation_node.value
        #get two object nodes
        obj1 = original_relation_node.get_children()[0]
        obj2 = original_relation_node.get_children()[1]
        #get the opposite relation value
        op_relation_type = get_opposite_relation(original_relation)
        op_relation = relation[op_relation_type][random.randint(0, 3)]
        #construct the new tree
        root = PPT(False)
        new_relation_node = PPT(op_relation)
        root.add_child(new_relation_node)
        new_relation_node.add_child(obj2)
        new_relation_node.add_child(obj1)

        return root


def add_attribute(input_PPT):
    #add an attribute to a node
    M_check = input_PPT.value
    if M_check:
        relation_nodes = input_PPT.get_children()
        new_relation_nodes = []
        for relation_node in relation_nodes:
            #get the attributes of two object nodes
            obj1 = relation_node.get_children()[0]
            obj2 = relation_node.get_children()[1]
            attr1 = obj1.get_children()
            attr2 = obj2.get_children()
            attr1_values = get_attribute_values(attr1)
            #check if the number of attributes is max or not
            if len(attr1_values) == 6:
                return input_PPT
            attr2_values = get_attribute_values(attr2)
            #construct the new subtree which is the same as the input tree
            new_relation_node = PPT(relation_node.value)
            new_obj1 = PPT(obj1.value)
            new_obj2 = PPT(obj2.value)
            new_relation_node.add_child(new_obj1)
            new_relation_node.add_child(new_obj2)
            for attr in attr1_values:
                new_obj1.add_child(PPT(attr))
            for attr in attr2_values:
                new_obj2.add_child(PPT(attr))
            #add new attribute to the tree
            new_attr1 = select_attribute(new_obj1.value)
            new_attr2 = select_attribute(new_obj2.value)
            if new_attr1 not in attr1_values:
                new_obj1.add_child(PPT(new_attr1))
            else:
                new_attr1 = select_attribute(new_obj1.value)
                while new_attr1 in attr1_values:
                    new_attr1 = select_attribute(new_obj1.value)
                new_obj1.add_child(PPT(new_attr1))

            if new_attr2 not in attr2_values:
                new_obj2.add_child(PPT(new_attr2))
            else:
                new_attr2 = select_attribute(new_obj2.value)
                while new_attr2 in attr2_values:
                    new_attr2 = select_attribute(new_obj2.value)
                new_obj2.add_child(PPT(new_attr2))
            new_relation_nodes.append(new_relation_node)
        root = PPT(True)
        for relation_node in new_relation_nodes:
            root.add_child(relation_node)
        return root
    else:
        relation_node = input_PPT.get_children()[0]
        relation = relation_node.value
        #get the attributes of two object nodes
        obj1 = relation_node.get_children()[0]
        obj2 = relation_node.get_children()[1]
        obj1_value = obj1.value
        obj2_value = obj2.value
        attr1 = obj1.get_children()
        attr2 = obj2.get_children()
        attr1_values = get_attribute_values(attr1)
        if len(attr1_values) == 6:
            return input_PPT
        attr2_values = get_attribute_values(attr2)
        #construct the new tree which is the same as the input tree
        root = PPT(False)
        new_relation_node = PPT(relation)
        root.add_child(new_relation_node)
        new_obj1 = PPT(obj1_value)
        new_obj2 = PPT(obj2_value)
        new_relation_node.add_child(new_obj1)
        new_relation_node.add_child(new_obj2)
        for attr in attr1_values:
            new_obj1.add_child(PPT(attr))
        for attr in attr2_values:
            new_obj2.add_child(PPT(attr))

        #add new attribute to the tree        
        new_attr1 = select_attribute(new_obj1.value)
        new_attr2 = select_attribute(new_obj2.value)
        if new_attr1 not in attr1_values:
            new_obj1.add_child(PPT(new_attr1))
        else:
            new_attr1 = select_attribute(new_obj1.value)
            while new_attr1 in attr1_values:
                new_attr1 = select_attribute(new_obj1.value)
            new_obj1.add_child(PPT(new_attr1))

        if new_attr2 not in attr2_values:
            new_obj2.add_child(PPT(new_attr2))
        else:
            new_attr2 = select_attribute(new_obj2.value)
            while new_attr2 in attr2_values:
                new_attr2 = select_attribute(new_obj2.value)
            new_obj2.add_child(PPT(new_attr2))
        return root
    
def check_ambiguity(relation_node, idx):
    if idx != 0:
        return False
    else:
        if relation_node.value in relation['top'] or relation_node in relation['bottom']:
            return True
        else:
            return False


def add_relation(input_PPT, related):
    #add a new relation subtree to the tree
    M_check = input_PPT.value
    if M_check:
        last_relation_node = input_PPT.get_children()[-1]
        new_relation_node = PPT(select_relation())
        #randomly select a related object node to the new relation node
        rand_idx = random.randint(0, 1)
        related_obj = last_relation_node.get_children()[rand_idx]
        related_obj = duplicate_subtree(related_obj)
        #avoid ambiguity
        if check_ambiguity(last_relation_node, rand_idx):
            related_obj = last_relation_node.get_children()[1]
        if related:
            new_obj = PPT(select_related_object(related_obj.value))
        else:
            new_obj = PPT(select_object())
        new_attr = select_attribute(new_obj.value)
        # new_color = select_color()
        new_number = select_number()
        obj_node_contruction(new_obj, new_attr, new_number)
        #construct the new subtree
        new_relation_node.add_child(related_obj)
        new_relation_node.add_child(new_obj)

        root = PPT(True)
        for relation_node in input_PPT.get_children():
            root.add_child(relation_node)
        root.add_child(new_relation_node)
        return root
    else:
        root = PPT(True)
        old_relation_node = input_PPT.get_children()[0]
        new_relation_node = PPT(select_relation())
        #randomly select a related object node to the new relation node
        rand_idx = random.randint(0, 1)
        related_obj = old_relation_node.get_children()[rand_idx]
        #avoid ambiguity
        if check_ambiguity(old_relation_node, rand_idx):
            related_obj = old_relation_node.get_children()[1]

        related_obj = duplicate_subtree(related_obj)
        if related:
            new_obj = PPT(select_related_object(related_obj.value))
        else:
            new_obj = PPT(select_object())
        new_attr = select_attribute(new_obj.value)
        new_color = select_color()
        new_number = select_number()
        obj_node_contruction(new_obj, new_attr, new_color, new_number)
        #construct the new subtree
        new_relation_node.add_child(related_obj)
        new_relation_node.add_child(new_obj)

        root.add_child(old_relation_node)
        root.add_child(new_relation_node)
        return root




    
