import requests
import json
import os
import time

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

    # 等待1小时
    time.sleep(3600)
