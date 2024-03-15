from simpletransformers.classification import MultiLabelClassificationModel, MultiLabelClassificationArgs
import time


# 預測情緒
def prediction(listTestData):
    # 輸出模型存在的目錄名稱
    # dir_name = './StoryTeller_docker/mood_analized/checkpoint-20000' 
    dir_name = '\\Marvin\\env\\src\\STT_SRC\\Mood\\outputs\\bert-epo-3-muti\\checkpoint-160000'
    # 自訂參數
    model_args = MultiLabelClassificationArgs()
    model_args.train_batch_size = 64
    model_args.num_train_epochs = 3
    model_args.output_attentions = True

    # 讀取 ClassificationModel
    model = MultiLabelClassificationModel(
        'bert', 
        f"{dir_name}", # 這裡要改成訓練完成的模型資料夾路徑
        use_cuda=True, 
        cuda_device=0, 
        num_labels=6, 
        args=model_args
    )

    # 預測
    predictions, raw_outputs = model.predict(listTestData)

    # 回傳預測結果，會是一個 list
    return raw_outputs[0]

def mood_ana_api(input_string):
    Data = [str(input_string)]
    ans = int(prediction(Data)[0])
    return ans
    

# 主程式
if __name__ == "__main__":
    # 計時開始
    tStart = time.time()

    # 準備預測情緒類別。語料可以不只一句！
    listTestData = [
        "考試超難的，我成績應該會很差"
    ]

    # 進行預測
    test = prediction(listTestData)
    print(test)
    # 計時結束
    tEnd = time.time()
    # 輸出程式執行的時間
    print(f"執行花費 {tEnd - tStart} 秒。")