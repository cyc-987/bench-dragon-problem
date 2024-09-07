import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件，指定文件路径
df = pd.read_csv('results/q4_50.csv')  # 请替换为你的实际文件名

# 忽略第一行，获取第二列和第三列数据
x = df.iloc[:, 1]  # 获取第二列
y = df.iloc[:, 2]  # 获取第三列

# 绘制散点图
plt.scatter(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Head of each board')
plt.show()