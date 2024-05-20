import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# 设置matplotlib的全局字体为Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16  # 也可以在这里设置全局字体大小

# 文件夹路径
folder_path = 'bandwidth'

# 用于存储每个服务器类型平均值的字典
averages = {'cloud server': [], 'edge server 1': [], 'edge server 2': []}
# 用于存储文件名中数字的列表
file_numbers = []

# 遍历文件夹中的所有CSV文件
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        # 从文件名提取第二个和第三个下划线之间的数字
        match = re.search(r'_(\d+)_', file)
        if match:
            file_number = int(match.group(1))
            file_numbers.append(file_number+5)

            # 读取CSV文件
            df = pd.read_csv(os.path.join(folder_path, file))
            # 计算每一列的平均值并存储
            for column in df.columns:
                averages[column].append(df[column].mean())

# 将文件名中的数字与平均值匹配并排序
sorted_indices = sorted(range(len(file_numbers)), key=lambda k: file_numbers[k])
sorted_file_numbers = [file_numbers[i] for i in sorted_indices]
for key in averages.keys():
    averages[key] = [averages[key][i] for i in sorted_indices]

plt.figure(figsize=(10, 8))

# 定义不同的线型
line_styles = ['-', '--', '-.']
colors = ['b', 'r', 'g']  # 可以为每种服务器类型指定不同的颜色
markers = ['o', 's', '^']  # 定义不同的标记样式
server_types = list(averages.keys())

for i, server_type in enumerate(server_types):
    plt.plot(sorted_file_numbers, averages[server_type], label=server_type,
             linestyle=line_styles[i % len(line_styles)], color=colors[i % len(colors)],
             marker=markers[i % len(markers)], markersize=8)  # 添加标记

plt.xlabel('The number of concurrent users', fontsize=20)
plt.ylabel('Bandwidth Consumption [Mbps]', fontsize=20)
# plt.title('Average Bandwidth Cost by Server Type', fontsize=16)
plt.legend(fontsize=20)
plt.grid(True)  # 添加网格
plt.xticks(fontsize=20)  # 设置x轴刻度的字体大小
plt.yticks(fontsize=20)  # 设置y轴刻度的字体大小
plt.savefig('bandwidth_consumption.png', dpi=600)  # DPI可以调整以获得所需的图像质量
plt.show()

# 可用带宽
bandwidths = {'cloud server': 40, 'edge server 1': 30, 'edge server 2': 30}

# 计算平均延时
delays = {server_type: [] for server_type in server_types}
cloud_server_avg_delay = sum(averages['cloud server']) / len(averages['cloud server']) / bandwidths['cloud server']
for server_type in ['edge server 1', 'edge server 2']:
    for avg_demand in averages[server_type]:
        # 对于edge server，延时包括了从cloud server到edge server的延时
        total_delay = avg_demand / bandwidths[server_type] + cloud_server_avg_delay
        delays[server_type].append(total_delay)

# 绘制延时折线图
plt.figure(figsize=(10, 8))

for i, server_type in enumerate(['edge server 1', 'edge server 2']):
    plt.plot(sorted_file_numbers, delays[server_type], label=server_type,
             linestyle=line_styles[i % len(line_styles)], color=colors[i % len(colors)],
             marker=markers[i % len(markers)], markersize=8)  # 添加标记

plt.xlabel('The number of concurrent users', fontsize=20)
plt.ylabel('Average Delay (s)', fontsize=20)
plt.legend(fontsize=20)
plt.grid(True)  # 添加网格
plt.xticks(fontsize=20)  # 设置x轴刻度的字体大小
plt.yticks(fontsize=20)  # 设置y轴刻度的字体大小
plt.savefig('average_delay.png', dpi=600)  # DPI可以调整以获得所需的图像质量
plt.show()


