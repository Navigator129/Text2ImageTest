import json

def analysis(path):
    with open(path, 'r') as f:
        data = json.load(f)
    err_num = 0
    total_num = len(data)
    idx_list = []
    idx = 0
    for dict_ in data:
        if type(dict_) == list:
            for d in dict_:
                if d['obj1'] and d['obj2'] and d['relation']:
                    continue
                else:
                    err_num += 1
                    idx_list.append(idx)
                    idx+=1
                    break
        else:
            if dict_['obj1'] and dict_['obj2'] and dict_['relation']:
                continue
            else:
                idx_list.append(idx)
                err_num += 1
        idx += 1
    correct_rate = 100 - err_num / total_num * 100
    return err_num, total_num, correct_rate, idx_list

def analysis_ab1(path):
    with open(path, 'r') as f:
        data = json.load(f)
    err_num = 0
    total_num = len(data)
    idx_list = []
    idx = 0
    for dict_ in data:
        if type(dict_) == list:
            for d in dict_:
                if d['obj1'] and d['obj2'] and d['relation']:
                    continue
                else:
                    err_num += 1
                    idx_list.append(idx)
                    idx+=1
                    break
        else:
            if dict_['obj1'] and dict_['obj2'] and dict_['relation']:
                continue
            else:
                idx_list.append(idx)
                err_num += 1
        idx += 1
    correct_rate = 100 - err_num / total_num * 100
    return err_num, total_num, correct_rate, idx_list

def analysis_ab2(path):
    with open(path, 'r') as f:
        data = json.load(f)
    err_num = 0
    total_num = len(data)
    idx_list = []
    idx = 0
    for dict_ in data:
        if type(dict_) == list:
            for d in dict_:
                if d['obj1'] and d['obj2']:
                    continue
                else:
                    err_num += 1
                    idx_list.append(idx)
                    idx+=1
                    break
        else:
            if dict_['obj1'] and dict_['obj2']:
                continue
            else:
                idx_list.append(idx)
                err_num += 1
        idx += 1

    correct_rate = 100 - err_num / total_num * 100
    return err_num, total_num, correct_rate, idx_list





def process_DALLE():
    path = './results/DALLE3/'
    total_num_sum = 0
    total_err = 0
    for i in range(1, 5):
        result = path + 'error_detect{}.json'.format(i)
        err_num, total_num, correct_rate = analysis(result)
        print('The correct rate for DALLE in experiment {} is {:.2f}%'.format(i, correct_rate))
        total_num_sum += total_num
        total_err += err_num
    print('The overall correct rate for DALLE is {:.2f}%'.format(100 - total_err / total_num_sum * 100))

def process_stable_diffusion(model):
    path = './results/Stable_Diffusion/{}/'.format(model)
    total_num_sum = 0
    total_err = 0
    for i in range(1, 5):
        result = path + 'error_detect{}.json'.format(i)
        err_num, total_num, correct_rate = analysis(result)
        print('The correct rate for model {} in experiment {} is {:.2f}%'.format(model, i, correct_rate))
        total_num_sum += total_num
        total_err += err_num
    print('The overall correct rate for model {} is {:.2f}%'.format(model, 100 - total_err / total_num_sum * 100))

def process_stable_diffusion_ablation1(model):
    path = './results/Stable_Diffusion/{}/ab1/'.format(model)
    total_num_sum = 0
    total_err = 0
    for i in range(1, 5):
        result = path + 'error_detect{}.json'.format(i)
        err_num, total_num, correct_rate = analysis_ab1(result)
        print('The correct rate for model {} in ablation 1 experiment {} is {:.2f}%'.format(model, i, correct_rate))
        total_num_sum += total_num
        total_err += err_num
    print('The overall correct rate for model {} is {:.2f}%'.format(model, 100 - total_err / total_num_sum * 100))

def process_stable_diffusion_ablation2(model):
    path = './results/Stable_Diffusion/{}/ab2/'.format(model)
    total_num_sum = 0
    total_err = 0
    for i in range(1, 5):
        result = path + 'error_detect{}.json'.format(i)
        err_num, total_num, correct_rate = analysis_ab1(result)
        print('The correct rate for model {} in ablation 2 experiment {} is {:.2f}%'.format(model, i, correct_rate))
        total_num_sum += total_num
        total_err += err_num
    print('The overall correct rate for model {} is {:.2f}%'.format(model, 100 - total_err / total_num_sum * 100))



def quick_test(model):
    if model == 'dalle':
        file_path0 = './results/DALLE3/quick_test_error_detect.json'
        file_path1 = './results/DALLE3/quick_test_ab1_error_detect.json'
        file_path2 = './results/DALLE3/quick_test_ab2_error_detect.json'
    elif model == 'v1-5' or model == 'v1-4' or model == 'v1-0':
        file_path0 = './results/Stable_Diffusion/{}/quick_test_error_detect.json'.format(model)
        file_path1 = './results/Stable_Diffusion/{}/quick_test_ab1_error_detect.json'.format(model)
        file_path2 = './results/Stable_Diffusion/{}/quick_test_ab2_error_detect.json'.format(model)
    else:
        file_path0 = './results/MidJourney/quick_test_error_detect.json'
        file_path1 = './results/MidJourney/quick_test_ab1_error_detect.json'
        file_path2 = './results/MidJourney/quick_test_ab2_error_detect.json'

    errnum0, totalnum0, correct_rate0,idx_list0 = analysis(file_path0)
    errnum1, totalnum1, correct_rate1,idx_list1 = analysis_ab1(file_path1)
    errnum2, totalnum2, correct_rate2,idx_list2 = analysis_ab2(file_path2)
 
    print('-----------------------------------')
    print('The correct rate for model {} is {:.2f}%'.format(model, correct_rate0))
    print('The correct rate for model {} in ablation 1 is {:.2f}%'.format(model, correct_rate1))
    print('The correct rate for model {} in ablation 2 is {:.2f}%'.format(model, correct_rate2))
    

    print('-----------------------------------')


if __name__ == '__main__':
    # process_DALLE()
    # process_stable_diffusion('v1-5')
    # process_stable_diffusion('v1-4')
    # process_stable_diffusion('v1-0')

    # process_stable_diffusion_ablation1('v1-5')
    # process_stable_diffusion_ablation1('v1-4')
    # process_stable_diffusion_ablation1('v1-0')

    # process_stable_diffusion_ablation2('v1-5')
    # process_stable_diffusion_ablation2('v1-4')
    # process_stable_diffusion_ablation2('v1-0')
    # quick_test('dalle')
    # quick_test('v1-5')
    # quick_test('v1-4')
    # quick_test('v1-0')
    quick_test('midjourney')