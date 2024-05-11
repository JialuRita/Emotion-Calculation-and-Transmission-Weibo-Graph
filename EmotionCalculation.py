import networkx as nx
from pymongo import MongoClient
import numpy as np
import csv
from scipy.stats import pearsonr
import random

# 构建网络
def read_graph(dataFilePath):
    G = nx.Graph()
    with open(dataFilePath, 'r') as file:
        data = [line.strip().split() for line in file]
    for line in data:
        # 每行表示一条边
        user1 = line[0]  # 用户1
        user2 = line[1]  # 用户2
        share = int(line[2])  # 转发数（连接强度）
        emotions = list(line[3])  # 用户1的情绪列表[愤怒, 厌恶, 高兴, 悲伤]
        G.add_edge(user1, user2, weight=share)
        G.nodes[user1]['emotions'] = emotions
    return G

# 保存最短路到数据库
def store_shortest_path_lengths_database(G):
    client = MongoClient('mongodb://localhost:27017')
    db = client['emotion_weibograph_db']
    collection = db['shortest_paths']
    collection.drop()
    # 计算并保存最短路
    for source, path_lengths in nx.all_pairs_shortest_path_length(G):
        for target, length in path_lengths.items():
            collection.insert_one({'source': source, 'target': target, 'length': length})

# 读取最短路径长度
def get_path_length(source, target):
    client = MongoClient('mongodb://localhost:27017')
    db = client['emotion_weibograph_db']
    collection = db['shortest_paths']
    result = collection.find_one({'source': source, 'target': target})
    if result:
        return result['length']
    else:
        return None  

# 计算pearsonr相关性
def correlation(data):
    bootstrap_samples = 10000
    bootstrap_correlations = [pearsonr(*zip(*[random.choice(data) for _ in range(len(data))]))[0] for _ in range(bootstrap_samples)]
    return np.mean(bootstrap_correlations), np.std(bootstrap_correlations)

# 计算情绪相关性
def emotion_correlation(G, h):
    anger = []
    disgust = []
    joy = []
    sad = []
    for i in G.node():
        for j in G.node():
            if i<j:
                path_length = get_path_length(i, j)
    if path_length == h:
                    anger.append([G.nodes[i]['emotions'][0], G.nodes[j]['emotions'][0]])
                    disgust.append([G.nodes[i]['emotions'][1], G.nodes[j]['emotions'][1]])
                    joy.append([G.nodes[i]['emotions'][2], G.nodes[j]['emotions'][2]])
                    sad.append([G.nodes[i]['emotions'][3], G.nodes[j]['emotions'][3]])
    anger_correlation, anger_error = correlation(anger)
    disgust_correlation, disgust_error = correlation(disgust)
    joy_correlation, joy_error = correlation(joy)
    sad_correlation, sad_error = correlation(sad)
    return (anger_correlation, anger_error), (disgust_correlation, disgust_error), (joy_correlation, joy_error), (sad_correlation, sad_error)



if __name__=='__main__':
    dataFilePath = "./data/weibograph.txt"
    G = read_graph(dataFilePath)  # 构建网络
    store_shortest_path_lengths_database(G)  # 保存最短路数据
    hs = [1, 2, 3, 4, 5]  # 特定距离1~5
    result = {}  # 保存结果
    for h in hs:
        result[h] = emotion_correlation(G, h)
    # 保存计算结果
    with open('./output/result.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        headers = ['h'] + [f'{emotion} Correlation, {emotion} Error' for emotion in ['Anger', 'Disgust', 'Joy', 'Sad']]
        writer.writerow(headers)
        for h, correlations in result.items():
            row = [h] + [value for stats in correlations.values() for value in stats]
            writer.writerow(row)
    