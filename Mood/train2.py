# train.py

from simpletransformers.classification import MultiLabelClassificationModel, MultiLabelClassificationArgs
import pandas as pd
import json
import time
import argparse

# 带入自定义的执行参数
parser = argparse.ArgumentParser(description='训练情绪分类语言模型')
parser.add_argument('--data', help='训练数据')
args = parser.parse_args()


# 读取训练数据
def getDataFrame():
    # 读取 JSON 文本结构
    with open(args.data, 'r', encoding="utf8") as file:
        listJson = json.loads(file.read())  # 将 JSON 转成数组

    # 将训练数据转成 panda DataFrame，并提供 headers
    df = pd.DataFrame(listJson, columns=["text", "label"])

    # 将标签列表转换为数字列表
    df["label"] = df["label"].apply(lambda x: [int(i) for i in x])

    # 回传 DataFrame
    return df

# 训练模型
def train(df):
    # 输出语言模型的目录名称
    dir_name = 'bert-base-chinese-bs-64-epo-3'

    # 自定义参数
    model_args = MultiLabelClassificationArgs()
    model_args.train_batch_size = 64
    model_args.num_train_epochs = 3
    model_args.output_dir = f"outputs/{dir_name}"

    # 建立 MultiLabelClassificationModel (会自动下载预训练模型)
    model = MultiLabelClassificationModel(
        'bert',  # 选择 bert (simple transformers 模型代码)
        'bert-base-chinese',  # 支持中文的 bert 预训练模型
        num_labels=6,  # multi-class 有 6 类，所以写 6
        args=model_args  # 带入自定义参数
    )

    # 训练 model
    model.train_model(df)

# 主程式
if __name__ == "__main__":
    tStart = time.time()
    df = getDataFrame()
    train(df)
    tEnd = time.time()
    print(f"执行花费 {tEnd - tStart} 秒。")
    # [0,0,0,0.5,0.5,0
