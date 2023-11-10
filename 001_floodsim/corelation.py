import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_data_backup\debug\tq38_london_strategy\static_waittodry\static_waittodry\final_output\7-30-am\7-30-am_450s_dtw_matching.csv'
df = pd.read_csv(path).iloc[::2]

# 计算协方差矩阵
covariance_matrix = df.cov()

# 打印协方差矩阵
print(covariance_matrix)

# 如果你还想看相关系数矩阵，可以用以下代码
correlation_matrix = df.corr()

# 使用Seaborn绘制热图
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()