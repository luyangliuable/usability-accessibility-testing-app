import os
import pandas as pd
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
import csv

from model import ResNet, Block
from get_data import Tappable

root_path = os.path.dirname(__file__)
img_dir = os.path.join(root_path, 'image_dir/')
dataset_path = os.path.join(root_path, 'dataset/tappability_dataset.csv')
model_path = os.path.join(root_path, 'model/resnet.pt')
model_stats_path = os.path.join(root_path, 'model/model_stats.csv')

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

batch_sze = 32
n_epochs = 1500
lr = 0.0005
momentum = 0.9
decay = 0.1

def train():
    dataset = pd.read_csv(dataset_path)
    train_data = dataset[dataset['split']=='train']
    test_data = dataset[dataset['split']=='test']

    train_dataset = Tappable(dataset= train_data, root_dir= img_dir)
    test_dataset = Tappable(dataset= test_data, root_dir= img_dir)

    dataloader_train = DataLoader(train_dataset, batch_size=batch_sze, shuffle=True, num_workers=4, pin_memory=True if DEVICE == "cuda" else False, prefetch_factor=4)
    dataloader_test = DataLoader(test_dataset, batch_size=batch_sze, shuffle=True, num_workers=4, pin_memory=True if DEVICE == "cuda" else False)

    model = ResNet(18, Block, 4, 2)
    model = model.to(DEVICE)

    criterion = torch.nn.CrossEntropyLoss().cuda()

    optimizer = optim.SGD(model.parameters(), lr=lr, nesterov=True, momentum = momentum)
    lr_scheduler = optim.lr_scheduler.MultiStepLR(optimizer=optimizer, milestones=[100,500,1000,1300], gamma=0.1)

    test_loss = []
    train_loss = []
    total_step_train = len(dataloader_train)
    total_step_test = len(dataloader_test)
    valid_loss_min = np.Inf

    # create csv and header + optimizer params
    with open(model_stats_path, 'w', newline='') as model_stats_file:
        writer = csv.writer(model_stats_file)
        header = [
            ['Batch Size','LR', 'Momentum', 'Decay'],
            [batch_sze, lr, momentum, decay],
            ['Epoch', 'Train Loss', 'Test Loss']
        ]
        writer.writerows(header)

    for epoch in range(1, n_epochs+1):
        model.train()
        running_loss = 0.0
        print(f'Epoch {epoch}\n')
        for batch_idx, item in enumerate(dataloader_train):
            inputs, labels = torch.as_tensor(item['image'], dtype=torch.float, device=torch.device(DEVICE)), torch.as_tensor(item['label'], dtype=torch.long, device=torch.device(DEVICE))
            optimizer.zero_grad(set_to_none=True)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if (batch_idx) % 20 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Train Loss: {:.4f}'
                    .format(epoch, n_epochs, batch_idx, total_step_train, loss.item()))
        train_loss.append(running_loss/total_step_train)
        lr_scheduler.step()

        model.eval()
        batch_loss = 0.0
        for batch_idx, item in enumerate(dataloader_test):
            data_t, target_t = torch.as_tensor(item['image'], dtype=torch.float, device=torch.device(DEVICE)), torch.as_tensor(item['label'], dtype=torch.long, device=torch.device(DEVICE))
            with torch.no_grad():
                outputs_t = model(data_t)
                loss_t = criterion(outputs_t, target_t)
                batch_loss += loss_t.item()
            if (batch_idx) % 20 == 0:
                    print('Epoch [{}/{}], Step [{}/{}], Test Loss: {:.4f}'
                        .format(epoch, n_epochs, batch_idx, total_step_test, loss_t.item()))

        test_loss.append(batch_loss/total_step_test)

        print(f'\ntrain-loss: {np.mean(train_loss):.4f}, test-loss: {np.mean(test_loss):.4f}')

        network_learned = batch_loss < valid_loss_min

        if network_learned:
            valid_loss_min = batch_loss
            torch.save(model.state_dict(), model_path)
            print('Improvement-Detected, save-model')
        
        # write epoch stats to csv
        with open(model_stats_path, 'a', newline='') as model_stats_file:
            writer = csv.writer(model_stats_file)
            writer.writerow([epoch, train_loss[epoch-1], test_loss[epoch-1]])


if __name__=='__main__':
    train()