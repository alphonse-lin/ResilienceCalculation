import gzip
from lxml import etree
import pandas as pd
from collections import defaultdict
import os


# 读取Matsim XML数据, 按照time_interval和link_id对数据进行分组
if __name__ == '__main__':
    # tag='7:30'
    tag_dic={"7:30":"7-30-am", "12:00":"12-00-pm", "16:30":"4-00-pm", "no":"no_event"}
    for tag in tag_dic.keys():
        dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_data_backup\debug\tq38_london_strategy\static_waittodry\static_waittodry'
        file_path = os.path.join(dir, f'output_{tag_dic[tag]}/ITERS/it.20/20.events.xml.gz')

        with gzip.open(file_path, 'rb') as gz:
            # 解压缩并读取XML内容
            xml_data = gz.read()

            # 使用lxml的etree解析XML数据
            events = etree.fromstring(xml_data)

            # 初始化一个记录计数的defaultdict
            link_counts = defaultdict(lambda: defaultdict(int))

            t_step = 450
            t_hours = 30
            t_count = t_hours * 3600 // t_step

            # 遍历所有事件
            for event in events:
                attris = event.attrib
                # 找到事件发生的时间间隔
                event_time = float(attris['time'])
                time_interval = (event_time // t_step)*t_step  # 使用整除得到时间间隔编号
                if attris['type'] == 'entered link':
                    # 在相应的时间间隔和link_id上增加计数
                    link_counts[time_interval][int(attris['link'])] += 1
                # elif attris['type'] == 'left link':
                #     # 在相应的时间间隔和link_id上增加计数
                #     link_counts[time_interval][int(attris['link'])] -= 1

            # 将defaultdict转换为list，然后创建DataFrame
            data = []
            for time_interval, links in link_counts.items():
                for link_id, count in links.items():
                    data.append([time_interval, link_id, count])

            # 创建DataFrame
            df_link_counts = pd.DataFrame(data, columns=['time_interval', 'link_id', 'count'])
            
            # 先确保time_interval是整型，以便正确排序列
            df_link_counts['time_interval'] = df_link_counts['time_interval'].astype(int)

            # 使用pivot方法重塑DataFrame
            pivot_df = df_link_counts.pivot(index='link_id', columns='time_interval', values='count')

            # 由于pivot可能会引入NaN，我们可以用0填充这些NaN值
            pivot_df = pivot_df.fillna(0)
            pivot_df.sort_values(by='link_id', inplace=True)
            
            # 确保索引是整数
            pivot_df.index = pivot_df.index.astype(int)

            # 创建一个完整的索引范围
            all_links = range(0, pivot_df.index.max() + 1)
            # 重新索引DataFrame，缺失的索引将会被填充NaN，然后用0替换这些NaN
            pivot_df_complete = pivot_df.reindex(all_links).fillna(0)

            out_dir=os.path.join(dir, f'final_output/{tag_dic[tag]}')
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            
            pivot_df_complete.to_csv(os.path.join(out_dir, f'{tag_dic[tag]}_450s.csv'))
            print(f"finish_{tag}")


