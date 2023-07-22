import requests
import json
import os
import time
import os
import shutil

output_dir=r'data\hereMap\mapdata_saved'
url = "https://data.traffic.hereapi.com/v7/flow?in=bbox:-0.50527,51.30094,0.32898,51.69871&locationReferencing=shape&apiKey=1AEUGec7CMNQBeURE3SFhHP0w4l--YYQnuTbMQerACg"

while True:
    response = requests.get(url)
    data = json.loads(response.text)

    record_time=data['sourceUpdated']
    output_file_path=os.path.join(output_dir, f'data_{record_time}.json').replace(':','_')

    with open(output_file_path, 'w') as f:
        print(output_file_path)
        json.dump(data, f)



    # 指定目标文件夹路径
    folder_path = "path/to/folder"

    # 获取文件夹中的所有文件名
    file_names = os.listdir(folder_path)

    # 判断文件数量是否超过 50
    if len(file_names) > 50:
        # 对文件名进行排序
        file_names.sort()
        # 需要删除的文件名列表
        delete_files = file_names[:40]
        # 遍历需要删除的文件名列表，删除文件
        for file_name in delete_files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # 等待1小时
    time.sleep(3600)
