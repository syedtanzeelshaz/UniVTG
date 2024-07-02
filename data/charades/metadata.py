import os
from tqdm import tqdm
import cv2
import sys
import pdb
import json
import pandas as pd

# for split in ['train']:
for split in ['train', 'test']:
    result = []
    # split = 'test'
    path = f'/data/home/qinghonglin/dataset/charades/Charades/charades_sta_{split}.txt'
    with open(path, 'r') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))

    vid_dir = '/data/home/qinghonglin/dataset/charades/videos/Charades_v1_480'
    f = open(f"/data/home/qinghonglin/dataset/charades/metadata/charades_{split}_fix.jsonl", 'w')

    for idx, data in enumerate(tqdm(result)):
        tmp = data[0].split('##')
        query = tmp[1]
        video = tmp[0].split(' ')[0]
        start, end = float(tmp[0].split(' ')[1]), float(tmp[0].split(' ')[2])

        cap = cv2.VideoCapture(os.path.join(vid_dir, video +'.mp4'))
        rate = cap.get(5)
        frame_num = cap.get(7)

        duration = frame_num / rate

        start = max(0, start)

        if end > duration+1:
            print(end, duration)
        end = min(end, duration)

        sample = {
        'qid': f'{split}{idx}',
        'query': query.lower(),
        'duration': duration,
        'vid': video,
        'relevant_windows': [[start, end]],
        }
        if start < end:
            f.write(json.dumps(sample))
            f.write('\n')
        else:
            print(video)
    f.close()
