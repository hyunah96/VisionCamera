import torch
print(torch.cuda.is_available())  # True 나와야 GPU 사용 가능
print(torch.version.cuda)           # PyTorch에서 인식하는 CUDA 버전 확인


