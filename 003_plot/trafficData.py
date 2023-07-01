import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
import numpy as np

if __name__ == '__main__':
    excel_path=r'data\input\rainfallData\ATC data selected dates Jul20_22.xlsx'
    # 读取 Excel 文件
    xl= pd.ExcelFile(excel_path)
    sheet_names = xl.sheet_names

    # 设置颜色映射
    # 定义起始和结束的 RGB 值
    start_rgb = [255, 0, 0] # 红色
    end_rgb = [0, 0, 255] # 蓝色

    # 将 RGB 值转换为浮点数
    start_rgb = np.array(start_rgb, dtype=float)
    end_rgb = np.array(end_rgb, dtype=float)

    for sheet_name in sheet_names:
        df = xl.parse(sheet_name)

        names=df['SiteNo'].unique()
        name_collections=[]
        plt.figure(figsize=(15, 6))
        name_size=len(names)
        index=0
        
        # difference=df['SiteNo'].astype(str).str.cat(df['DIRECN2'], sep='-').unique()
        # # 生成渐变的 RGB 列表
        # n = len(difference)
        # rgb_list = []
        # for i in range(n):
        #     # 计算当前位置的 RGB 值
        #     rgb = start_rgb * (1 - i/n) + end_rgb * (i/n)
        #     # 将 RGB 值转换为整数，并添加到列表中
        #     rgb_list.append(np.array(rgb/255, dtype=float))
    
        for name in names:
            name_desribe=[]
            name_df=df[df['SiteNo']==name]
            directions=name_df['DIRECN2'].unique()
            directions_size=len(directions)
            col = [np.random.random(), np.random.random(), np.random.random()]
            for direction in directions:
                temp_df=name_df[name_df['DIRECN2']==direction]
                name_collections.append(f'{name}_{direction}')
                name_desribe.append(f'{name}_{direction}')
                temp_df['Date'] = pd.to_datetime(temp_df['Date'])
                temp_df = temp_df.sort_values(by=['Date', 'StartHour'], ascending=[True, True])

                # 将两列数据连接成一列
                temp_df['StartHour'] = temp_df['StartHour'].astype(str)
                # 将日期列转换为 Pandas 的 datetime 类型，将日期格式化为只包含月份的字符串
                temp_df['newDate'] = temp_df['Date'].dt.strftime('%y%m%d')
                temp_df['newDate'] = temp_df['newDate'].astype(str)
                temp_df['newDate'] = temp_df['newDate'].str.cat(temp_df['StartHour'], sep='-')

                # 设置 x 轴和 y 轴的数据
                # 将数字列转换为字符串列

                x = temp_df['newDate']
                y = temp_df['Volume']

                # 绘制折线图
                plt.plot(x, y,color=col)
                col=[x * 0.5 for x in col]
            #  # 设置 x 轴标签和标题
            # plt.xlabel('Date and Hour')
            # plt.title(f'{sheet_name}_{name}_Volume by Date')

            # plt.xticks(temp_df['newDate'][::24])
            
            # plt.legend(name_desribe, bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., title="RoadNo",fontsize=10)
            
            # plt.savefig(f'data/output/trafficFlow/{sheet_name}_{name}_VolumeByDate.png',dpi=300,bbox_inches='tight')
            # plt.clf()

        # 设置 x 轴标签和标题
        plt.xlabel('Date and Hour')
        plt.title(f'{sheet_name}_Volume by Date')

        plt.xticks(temp_df['newDate'][::24])
        
        plt.legend(name_collections, bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., title="RoadNo",fontsize=10)
        
        plt.savefig(f'data/output/trafficFlow/{sheet_name}_VolumeByDate.png',dpi=300,bbox_inches='tight')
