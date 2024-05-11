import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
anger_files = [f"./output/pearson_anger_distance_{i}.csv" for i in range(1, 6)]
disgust_files = [f"./output/pearson_disgust_distance_{i}.csv" for i in range(1, 6)]
joy_files = [f"./output/pearson_joy_distance_{i}.csv" for i in range(1, 6)]
sad_files = [f"./output/pearson_sad_distance_{i}.csv" for i in range(1, 6)]

anger_data = [pd.read_csv(file) for file in anger_files]
disgust_data = [pd.read_csv(file) for file in disgust_files]
joy_data = [pd.read_csv(file) for file in joy_files]
sad_data = [pd.read_csv(file) for file in sad_files]

anger_correlations = [df['mean_correlation'].mean() for df in anger_data]
disgust_correlations = [df['mean_correlation'].mean() for df in disgust_data]
joy_correlations = [df['mean_correlation'].mean() for df in joy_data]
sad_correlations = [df['mean_correlation'].mean() for df in sad_data]

# 距离取值1~5
x_values = range(1, 6)

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(x_values, anger_correlations, marker='o', color='red', label='Anger')
plt.plot(x_values, disgust_correlations, marker='*', color='green', label='Disgust')
plt.plot(x_values, joy_correlations, marker='^', color='orange', label='Joy')
plt.plot(x_values, sad_correlations, marker='s', color='blue', label='Sad')
plt.xlabel('Distance($h$)')
plt.ylabel('Mean Pearson Correlation')
plt.title('Correlation for Emotions over Distance')
plt.legend()
plt.grid(True, linestyle='--')
# 保存图像
plt.savefig("./image/pearson_correlation_distance.png")
plt.show()