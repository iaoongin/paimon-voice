
import torch

def check_cuda():
    print(torch.zeros(1).cuda())
    print(torch.cuda.is_available())

    assert not torch.zeros(1).cuda()
    assert torch.cuda.is_available()

check_cuda()