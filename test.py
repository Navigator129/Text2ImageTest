
from numpy import array, float32
from tqdm import tqdm



detect_result = [{'detect cls': ['chair', 'person', 'person', 'chair', 'chair', 'person', 'chair', 'chair', 'chair','chair', 'chair', 'person', 'chair', 'chair',
   'chair', 'dining table', 'chair', 'chair', 'person', 'train', 'person', 'chair', 'chair', 'chair', 'chair', 'person', 'chair', 'chair', 'chair', 'chair','chair',
   'chair', 'chair'],
  'detect box': [[0.12, 333.17, 204.49, 510.53],
   [249.13, 187.47, 263.21, 218.18],
   [207.44, 194.96, 226.7, 212.37],
   [216.42, 215.82, 250.49, 236.88],
   [135.73, 234.59, 207.68, 263.06],
   [167.99, 203.64, 193.16, 225.98],
   [0.02, 294.44, 56.66, 445.33],
   [350.62, 235.27, 390.47, 309.82],
   [267.37, 331.42, 467.68, 510.58],
   [267.03, 257.88, 374.69, 331.58],
   [376.0, 242.37, 446.13, 311.69],
   [212.53, 199.12, 234.55, 216.22],
   [436.04, 290.59, 512.1, 377.61],
   [374.74, 243.99, 448.05, 353.06],
   [351.37, 233.68, 388.35, 259.81],
   [251.8, 206.22, 320.37, 225.4],
   [38.75, 239.44, 112.79, 308.44],
   [328.94, 219.32, 354.09, 256.24],
   [205.58, 194.97, 220.46, 208.93],
   [-0.13, 0.74, 511.87, 510.43],
   [183.89, 202.47, 202.75, 221.0],
   [109.63, 259.4, 222.2, 339.74],
   [270.23, 231.92, 345.39, 261.72],
   [269.79, 231.83, 346.6, 262.85],
   [38.71, 238.08, 126.09, 344.78],
   [191.87, 203.43, 213.06, 222.17],
   [424.11, 292.99, 512.1, 510.07],
   [164.11, 222.56, 221.34, 260.79],
   [138.98, 218.1, 170.35, 242.64],
   [216.26, 235.78, 271.94, 294.01],
   [253.17, 215.74, 318.1, 240.52],
   [266.08, 224.67, 328.17, 245.78],
   [187.24, 299.3, 292.08, 427.26]]}]

relation_dic = {"top": ['on top of', 'above', 'Atop', 'Upon'], "bottom": ["Beneath", "Under", "Below", "Underneath"], 
            "left": ["To the left of","On the left side of", "Leftward of", "Adjacent to the left of"], 
            "right": ["To the right of", "On the right side of", "Rightward of", "Adjacent to the right of"]}

number = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
PPTs = [{'relation': 'Underneath',
 'obj1': 'train',
 'obj1_attr': ['smoking', 'orange', 'six'],
 'obj2': 'chair',
 'obj2_attr': ['comfortable', 'white', 'two']}]

#input [Xmin, Ymax] [Xmax, Ymin]
#middle_point = [(Xmax + Xmin)/2, (Ymax+Ymin)/2]
#step 1: check obj
def detect_object(obj1, obj2, fetch_result):
  #check the targeted objs exist or not
    object_detected = fetch_result['detect cls']
    dict_ = {}
    if obj1 not in object_detected:
        dict_['obj1'] = False
    else:
        dict_['obj1'] = True
    if obj2 not in object_detected:
        dict_['obj2'] = False
    else:
        dict_['obj2'] = True
    return dict_

def detect_number(obj1, obj2, obj1_num, obj2_num, fetch_result, dict_):
  #check the number of objs correct or not
    if not dict_['obj1']:
        dict_['obj1_num'] = False
    if not dict_['obj2']:
        dict_['obj2_num'] = False

  
    object_detected = fetch_result['detect cls']
    count_ = {}
    for obj in object_detected:
      count_[obj] = count_.get(obj, 0) + 1
    if dict_['obj1']:
        if count_[obj1] == obj1_num:
            dict_['obj1_num'] = True
        else:
            dict_['obj1_num'] = False
    
    if dict_['obj2']:
        if count_[obj2] == obj2_num:
            dict_['obj2_num'] = True
        else:
            dict_['obj2_num'] = False

    return dict_

def get_relation_type(relation):
    left = relation_dic['left']
    right = relation_dic['right']
    top = relation_dic['top']
    bottom = relation_dic['bottom']
    if relation in left:
        return 'left'
    if relation in right:
        return 'right'
    if relation in top:
        return 'top'
    if relation in bottom:
        return 'bottom'
   
def check_relation(relation_type, obj1_points, obj2_points, dict_):
    if relation_type == 'top':
        obj1_botmost_point = min(obj1_points, key=lambda point: point[1])
        obj2_topmost_point = max(obj2_points, key=lambda point: point[1])
        #Y1min >= Y2max
        if obj1_botmost_point[1] >= obj2_topmost_point[1]:
            dict_['relation'] = True
        else:
            dict_['relation'] = False
        return dict_
    
    if relation_type == 'bottom':
        obj1_topmost_point = max(obj1_points, key=lambda point: point[1])
        obj2_botmost_point = min(obj2_points, key=lambda point: point[1])
        #Y1max <= Y2min
        if obj1_topmost_point[1] <= obj2_botmost_point[1]:
            dict_['relation'] = True
        else:
            dict_['relation'] = False
        return dict_
    if relation_type == 'left':
        obj1_rightmost_point = max(obj1_points, key=lambda point: point[0])
        obj2_leftmost_point = min(obj2_points, key=lambda point: point[0])
        #X1max <= X2min
        if obj1_rightmost_point[0] <= obj2_leftmost_point[0]:
            dict_['relation'] = True
        else:
            dict_['relation'] = False
        return dict_
    if relation_type == 'right':
        obj1_leftmost_point = min(obj1_points, key=lambda point: point[0])
        obj2_rightmost_point = max(obj2_points, key=lambda point: point[0])
        #X1min >= X2max
        if obj1_leftmost_point[0] >= obj2_rightmost_point[0]:
            dict_['relation'] = True
        else:
            dict_['relation'] = False
        return dict_
    
    return dict_

def detect_relation(relation, fetch_result, obj1, obj2, dict_):
    #check the relation correct or not
    relation_type = get_relation_type(relation)

    #check if needed to check the relation
    if not dict_['obj1'] or not dict_['obj2']:
        dict_['relation'] = False
        return dict_
    
    #get each object's middle point
    object_list = fetch_result['detect cls']
    axis_list = fetch_result['detect box']
    i = 0

    object_point = {}
    for axis in axis_list:
        
        Xmin, Ymax, Xmax, Ymin = axis[0], axis[1], axis[2], axis[3]
        middle_point = [(Xmax + Xmin)/2, (Ymax+Ymin)/2]
        if not object_point.get(object_list[i]):
            object_point[object_list[i]] = [middle_point]
        else:
            object_point[object_list[i]].append(middle_point)

        i += 1
    
    obj1_points = object_point[obj1]
    obj2_points = object_point[obj2]
    dict_ = check_relation(relation_type, obj1_points, obj2_points, dict_)

    return dict_
       

def get_number(list_):
  for element in list_:
    if element in number:
      num = number.index(element) + 1
      return num
  
  return False


def get_component(PPT):
  obj1 = PPT['obj1']
  obj2 = PPT['obj2']
  obj1_attr = PPT['obj1_attr']
  obj2_attr = PPT['obj2_attr']
  obj1_num = get_number(obj1_attr)
  obj2_num = get_number(obj2_attr)
  relation = PPT['relation']

  return obj1, obj2, obj1_num, obj2_num, relation


def check_error(PPTs, detect_result):
    results = []
    error_detect = {}
    for i in tqdm(range(len(PPTs))):
        test_case = PPTs[i]
        obj1, obj2, obj1_num, obj2_num, relation = get_component(test_case)
        error_detect = detect_object(obj1, obj2, detect_result[i])
        error_detect = detect_number(obj1, obj2, obj1_num, obj2_num, detect_result[i], error_detect)
        error_detect = detect_relation(relation, detect_result[i], obj1, obj2, error_detect)
        results.append(error_detect)
    print(results)
#   file_path = '/content/drive/MyDrive/Image_Test/results.json'
#   with open(file_path, 'w') as f:
#     json.dump(results, f, indent=4)


# def test():
#   results = []
#   error_detect = {}
#   for i in range(len(list)):
#     test_case = list[i]
#     obj1, obj2, obj1_num, obj2_num, relation = get_component(test_case)
#     error_detect = detect_object(obj1, obj2, detect_result[i])
#     error_detect = detect_number(obj1, obj2, obj1_num, obj2_num, detect_result[i], error_detect)
#     error_detect = detect_relation(relation, detect_result[i], obj1, obj2, error_detect)
#     results.append(error_detect)

    

check_error(PPTs, detect_result)
