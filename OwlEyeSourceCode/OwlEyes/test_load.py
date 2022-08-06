from network import Net
import torch
import numpy as np
import torch.nn as nn
import os

model_dir = './model/4model.pth'
model = Net()

if __name__ == '__main__':
    model = nn.DataParallel(model)
    model.load_state_dict(torch.load(model_dir,map_location=torch.device('cpu'))) 