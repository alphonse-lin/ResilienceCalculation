import os
import re
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utilis.general import timeCount, mkdir, getfiles
import shutil
import pandas as pd

if __name__ == '__main__':
    # 第五步：整合matsim结果
    target_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\output\dynamic_12_00_pm'
    new_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\analysis'
    checked=[]
    files=getfiles(target_dir)
    img_name='20.legHistogram_all.png'
    txt_name='20.legHistogram.txt'
    csv_record=os.path.join(new_dir,'record.csv')
    record_file_name=[]
    record_en_route_all=[]
    record_time=[]
    for file in files:
        file_path=os.path.join(target_dir,file,'ITERS','it.20')
        ori_image_path=os.path.join(file_path,img_name)
        new_image_path=os.path.join(new_dir,img_name)
        
        # 使用shutil库移动文件
        if os.path.exists(new_image_path):
            os.remove(new_image_path)
        if os.path.exists(ori_image_path):
            shutil.copy(ori_image_path, new_image_path)
        else:
            continue
        # 指定新的文件名
        new_name = os.path.join(new_dir,f'legHistogram_{file}.png')

        # 使用os库重命名文件
        os.rename(new_image_path, new_name)

        txt_path=os.path.join(file_path,txt_name)
        txt_df=pd.read_csv(txt_path,sep='	')
        # 使用pandas的query方法根据条件筛选出符合条件的行
        filtered_df = txt_df.query('43200 <= `time.1` <= 55800')

        # 找到筛选后的数据中stuck_all最大的数
        max_stuck_all = filtered_df['en-route_all'].max()
        max_row=filtered_df[filtered_df['en-route_all'] == filtered_df['en-route_all'].max()]
        # print(max_row)
        time = max_row['time'].values[0]
        record_file_name.append(file)
        record_en_route_all.append(max_stuck_all)
        record_time.append(time)
    record_df=pd.DataFrame({'file_name':record_file_name,'en_route_all':record_en_route_all,'time':record_time})
    record_df.to_csv(csv_record,index=False)