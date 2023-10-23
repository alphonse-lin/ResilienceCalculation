import pandas as pd
import os
import numpy as np
import warnings

if __name__ == "__main__":
    # 禁用所有警告
    warnings.filterwarnings('ignore')
    # 将科学计数法输出关闭
    np.set_printoptions(suppress=True)
    # 第四步：重构数据
    base_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy'
    score_csv=os.path.join(base_dir, 'network_importance_normalized.csv')
    score_df=pd.read_csv(score_csv)

    # create a duplicate dataframe
    df_duplicate = score_df.copy()

    # increment id by 1 in the duplicate
    df_duplicate['id'] += 1

    # concatenate original and duplicate, then sort by id
    df_final = pd.concat([score_df, df_duplicate]).sort_values(by='id').reset_index(drop=True)

    # df_final.to_csv(os.path.join(base_dir, 'network_importance_final.csv'), index=False)

    debug=1/df_final['m_ch_500']*60
    print(debug.describe())
    
