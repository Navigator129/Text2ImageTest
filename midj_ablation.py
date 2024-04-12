import json
import midj_generator as mg
Channel_id1 = [1228124992714178590, 1228125034216816651, 1228125057122045992, 1228125074360635392] 
Channel_id2 = [1228125107042652261, 1228125128718811256, 1228125142421344397, 1228125156577382540]
def open_file(i, ab):
    file_path = './files/exp{}/ablation/ablation{}.json'.format(i, ab)
    print('opening file {}'.format(file_path))
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def process():
    for i in range(1,3):
        for j in range(1, 5):
            prompts = open_file(j, i)
            if i == 1:
                channel_id = Channel_id1[j-1]
            else:
                channel_id = Channel_id2[j-1]
            if type(prompts) == list:
                pass
            else:
                for prompt in prompts:
                    mg.compensate(prompt, channel_id)
if __name__ == '__main__':
    process()