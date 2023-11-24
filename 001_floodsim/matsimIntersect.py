import pandas as pd
import os

if __name__ == '__main__':
    tag_dic={"7:30":"7-30-am", "12:00":"12-00-pm", "16:30":"4-00-pm"}
    # tag_dic={"7:30":"7-30-am", "12:00":"12-00-pm", "16:30":"4-00-pm", "no":"no_event"}
    time_dic={"7:30":7.5, "12:00":12, "16:30":16.5}
    parent_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_data_backup\debug\tq38_london_strategy\static_waittodry\static_waittodry\final_output'
    
    for tag in tag_dic.keys():
        tag_name=tag_dic[tag]
        input_dir=os.path.join(parent_dir,tag_name)
    
        l_stat_file_name=f'{tag_name}_merged_output.csv'
        l_count_file_name=f'{tag_name}_450s.csv'

        #region 读取link_stat文件
        l_stat_path=os.path.join(input_dir,l_stat_file_name)
        l_df=pd.read_csv(l_stat_path)
        l_df=l_df.iloc[:, [0] + list(range(25, l_df.shape[1]))]
        #endregion

        # region 读取link_count文件
        ti_tag=tag
        # 输入小时数
        input_hours = time_dic[ti_tag]
        # 将小时转换为秒
        start_second = input_hours * 3600
        end_second = (input_hours + 2) * 3600
        
        link_count_path=os.path.join(input_dir,l_count_file_name)
        lc_df=pd.read_csv(link_count_path)
        # 确保'link_id'列在DataFrame中
        assert 'link_id' in lc_df.columns, "'link_id' does not exist in the DataFrame"

        # 筛选出符合条件的列名，同时保留'link_id'
        sel_col = ['link_id'] + [col for col in lc_df.columns[1:] if isinstance(col, str) and start_second <= int(col) <= end_second]
        # # 使用筛选出的列名来索引df
        sel_lc_df = lc_df[sel_col]
        #endregion

        merged_df=pd.merge(sel_lc_df,l_df, left_on='link_id',right_on='LINK',how='left')
        merged_df.drop('LINK',axis=1,inplace=True)
        merged_df.fillna(0,inplace=True)
        merged_df.to_csv(os.path.join(input_dir, f'{tag_name}_450s_link_count+choice.csv'),index=False)
        print(f'finished_{tag_name}')