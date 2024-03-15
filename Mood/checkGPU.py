import torch
print(torch.__version__)

print(torch.version.cuda)
print(torch.backends.cudnn.version())
if torch.cuda.is_available():
    print("目前 GPU 代號: " + str(torch.cuda.current_device()))
else:
    print("不支援 GPU")
