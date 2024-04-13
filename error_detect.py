
import json
from tqdm import tqdm


def get_PPTs(i):
    final_prompts = []
    final_PPTs = []
    relate_seed_path = './files/exp{}/related_seed_prompts.json'.format(i)
    unrelated_seed_path = './files/exp{}/unrelated_seed_prompts.json'.format(i)
    related_mutate_path = './files/exp{}/related_mutate_prompts.json'.format(i)
    unrelated_mutate_path = './files/exp{}/unrelated_mutate_prompts.json'.format(i)
    prompts, PPTs = fetch_prompt_and_PPTs(relate_seed_path)
    final_prompts.extend(prompts)
    final_PPTs.extend(PPTs)
    prompts, PPTs = fetch_prompt_and_PPTs(unrelated_seed_path)
    final_prompts.extend(prompts)
    final_PPTs.extend(PPTs)
    prompts, PPTs = fetch_prompt_and_PPTs(related_mutate_path)
    final_prompts.extend(prompts)
    final_PPTs.extend(PPTs)
    prompts, PPTs = fetch_prompt_and_PPTs(unrelated_mutate_path)
    final_prompts.extend(prompts)
    final_PPTs.extend(PPTs)
    return final_prompts, final_PPTs

def fetch_prompt_and_PPTs(path):
    prompts = []
    PPTs = []
    with open(path, 'r') as f:
        dict_ = json.load(f)
    for prompt_dict in dict_:
        if prompt_dict['validity'].lower() == 'valid':
            prompts.append(prompt_dict['prompt'])
            PPTs.append(prompt_dict['PPT'])
    return prompts, PPTs

def get_detect_result(path):
    with open(path, 'r') as f:
        results = json.load(f)
    return results


relation_dic = {"top": ['on top of', 'above', 'Atop', 'Upon'], "bottom": ["Beneath", "Under", "Below", "Underneath"], 
            "left": ["To the left of","On the left side of", "Leftward of", "Adjacent to the left of"], 
            "right": ["To the right of", "On the right side of", "Rightward of", "Adjacent to the right of"]}



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
        obj1_topmost_point = max(obj1_points, key=lambda point: point[1])
        obj2_botmost_point = min(obj2_points, key=lambda point: point[1])
        #Y1min >= Y2max
        if obj1_topmost_point[1] <= obj2_botmost_point[1]:
            dict_['relation'] = True
        else:
            dict_['relation'] = False
        return dict_
    
    if relation_type == 'bottom':
        obj1_botmost_point = min(obj1_points, key=lambda point: point[1])
        obj2_topmost_point = max(obj2_points, key=lambda point: point[1])
        #Y1max <= Y2min
        if obj1_botmost_point[1] >= obj2_topmost_point[1]:
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
        
        Xmin, Ymin, Xmax, Ymax = axis[0], axis[1], axis[2], axis[3]
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
       

def get_component(PPT):
  obj1 = PPT['obj1']
  obj2 = PPT['obj2']
  relation = PPT['relation']

  return obj1, obj2, relation


def check_error(PPTs, detect_result, paths):
    results = []
    error_detect = {}
    for i in tqdm(range(len(PPTs))):
        test_case = PPTs[i]['PPT']
        if type(test_case) == list:
            tc_results = []
            for tc in test_case:
                obj1, obj2, relation = get_component(tc)
                error_detect = detect_object(obj1, obj2, detect_result[i])
                error_detect = detect_relation(relation, detect_result[i], obj1, obj2, error_detect)
                tc_results.append(error_detect)
            results.append(tc_results)
        else:
            obj1, obj2, relation = get_component(test_case)
            error_detect = detect_object(obj1, obj2, detect_result[i])
            error_detect = detect_relation(relation, detect_result[i], obj1, obj2, error_detect)
            results.append(error_detect)
    save_results(results, paths)

def check_error_midj(PPTs, detect_result, paths):
    results = []
    error_detect = {}
    for i in tqdm(range(100)):
        test_case = PPTs[i]['PPT']
        if type(test_case) == list:
            tc_results = []
            for tc in test_case:
                obj1, obj2, relation = get_component(tc)
                for j in range(i*4, (i+1)*4):
                    error_detect = detect_object(obj1, obj2, detect_result[j])
                    error_detect = detect_relation(relation, detect_result[j], obj1, obj2, error_detect)
                    tc_results.append(error_detect)
            results.append(tc_results)
        else:
            for j in range(i*4, (i+1)*4):
                obj1, obj2, relation = get_component(test_case)
                error_detect = detect_object(obj1, obj2, detect_result[j])
                error_detect = detect_relation(relation, detect_result[j], obj1, obj2, error_detect)
                results.append(error_detect)
    save_results(results, paths)



def check_error_with_missing(PPTs, detect_result, paths, missing_idx):
    results = []
    error_detect = {}
    idx = 0
    for i in tqdm(range(len(PPTs))):
        if i in missing_idx:
            continue
        test_case = PPTs[i]
        if type(test_case) == list:
            tc_results = []
            for tc in test_case:
                obj1, obj2, relation = get_component(tc)
                error_detect = detect_object(obj1, obj2, detect_result[idx])
                error_detect = detect_relation(relation, detect_result[idx], obj1, obj2, error_detect)
                tc_results.append(error_detect)
            results.append(tc_results)
        else:
            obj1, obj2, relation = get_component(test_case)
            error_detect = detect_object(obj1, obj2, detect_result[idx])
            error_detect = detect_relation(relation, detect_result[idx], obj1, obj2, error_detect)
            results.append(error_detect)
        idx += 1
    save_results(results, paths)


def save_results(results, paths):
    with open(paths, 'w') as f:
        json.dump(results, f, indent=4)

def process_stable_diffsuion(model):
    path = './results/Stable_Diffusion/{}/'.format(model)
    print('processing {}'.format(model))
    for i in range(1,5):
        prompts, PPTs = get_PPTs(i)
        object_detection_path = path + 'exp{}.json'.format(i)
        detect_result = get_detect_result(object_detection_path)
        check_error(PPTs, detect_result, path + 'error_detect{}.json'.format(i))
        print('Exp{} Done!'.format(i))

def process_DALLE():
    path = './results/DALLE3/'
    print('processing DALLE3')
    missing_idx1 = [216]
    missing_idx2 = []
    missing_idx3 = [72, 167, 424, 438]
    missing_idx4 = [415]
    for i in range(1,5):
        prompts, PPTs = get_PPTs(i)
        object_detection_path = path + 'exp{}.json'.format(i)
        detect_result = get_detect_result(object_detection_path)
        if i == 1:
            check_error_with_missing(PPTs, detect_result, path + 'error_detect{}.json'.format(i), missing_idx1)
        elif i == 2:
            check_error_with_missing(PPTs, detect_result, path + 'error_detect{}.json'.format(i), missing_idx2)
        elif i == 3:
            check_error_with_missing(PPTs, detect_result, path + 'error_detect{}.json'.format(i), missing_idx3)
        else:
            check_error_with_missing(PPTs, detect_result, path + 'error_detect{}.json'.format(i), missing_idx4)
        print('Exp{} Done!'.format(i))



def process_quick_test(model):
    ppt_base_path = './files/test.json'
    ppt_ab1_pah = './files/ablation1.json'
    ppt_ab2_path = './files/ablation2.json'
    if model == 'dalle':
        file_path0 = './results/DALLE3/quick_test.json'
        file_path1 = './results/DALLE3/quick_test_ab1.json'
        file_path2 = './results/DALLE3/quick_test_ab2.json'
    elif model == 'v1-5' or model == 'v1-4' or model == 'v1-0':
        file_path0 = './results/Stable_Diffusion/{}/quick_test.json'.format(model)
        file_path1 = './results/Stable_Diffusion/{}/quick_test_ab1.json'.format(model)
        file_path2 = './results/Stable_Diffusion/{}/quick_test_ab2.json'.format(model)
    else:
        file_path0 = './results/Midjourney/quick_test.json'.format(model)
        file_path1 = './results/Midjourney/quick_test_ab1.json'.format(model)
        file_path2 = './results/Midjourney/quick_test_ab2.json'.format(model)
        


    with open(ppt_base_path, 'r') as f:
        ppt_base = json.load(f)
    with open(ppt_ab1_pah, 'r') as f:
        ppt_ab1 = json.load(f)
    with open(ppt_ab2_path, 'r') as f:
        ppt_ab2 = json.load(f)

    detect_result0 = get_detect_result(file_path0)
    detect_result1 = get_detect_result(file_path1)
    detect_result2 = get_detect_result(file_path2)

    if model == 'midjourney':
        check_error_midj(ppt_base, detect_result0, file_path0.replace('.json', '_error_detect.json'))
        check_error_midj(ppt_ab1, detect_result1, file_path1.replace('.json', '_error_detect.json'))
        check_error_midj(ppt_ab2, detect_result2, file_path2.replace('.json', '_error_detect.json'))
    else:
        check_error(ppt_base, detect_result0, file_path0.replace('.json', '_error_detect.json'))
        check_error(ppt_ab1, detect_result1, file_path1.replace('.json', '_error_detect.json'))
        check_error(ppt_ab2, detect_result2, file_path2.replace('.json', '_error_detect.json'))

    print('Done!')



if __name__ == '__main__':
    # process_stable_diffsuion('v1-5')
    # process_stable_diffsuion('v1-4')
    # process_stable_diffsuion('v1-0')
    # process_DALLE()
    # process_quick_test('dalle')
    # process_quick_test('v1-5')
    # process_quick_test('v1-4')
    # process_quick_test('v1-0')
    process_quick_test('midjourney')
    print('Done!')
