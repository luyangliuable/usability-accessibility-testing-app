import os
import numpy as np
import torch
from torch.utils.data import Dataset
from skimage import io, transform
import torchvision
from torchvision import transforms

from os import path


# Image tranformation
class applyMask(object):

    """
    Matrix multiplication of the RGB image and a binary mask of the object
    """

    def __call__(self, sample):
        
        image = sample['image']
        
        binary_mask = np.zeros(shape=(image.shape[0], image.shape[1]))
        x_min = sample['x_min']
        x_max = sample['x_max']
        y_min = sample['y_min']
        y_max = sample['y_max']
        
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                    binary_mask[y,x] = 1 #sets binary mask value to 1 if within tappable bounds

        concat = np.dstack((image, binary_mask)) #matrix multiplication of image and binary mask
    
        return {'image': concat, 'label': sample['label']}


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, label = sample['image'], sample['label']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C x H x W
        image = image.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'label': label}

dataTransform = transforms.Compose([applyMask(), ToTensor()])

class Tappable(Dataset):
    """
    Creates dataset from the csv of labelled image and object ids
    """

    def __init__(self,root_dir, dataset):
        self.root_dir = root_dir
        self.transform = dataTransform
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        # check if tensor is saved
        tensor_path = 'D:/tappability_tensor_data/' + str(idx) + '.pt'
        if path.exists(tensor_path):
            return torch.load(tensor_path)
        
        image_id = self.dataset.iloc[idx, 0]
        object_id = self.dataset.iloc[idx, 1]

        img_name = os.path.join(self.root_dir, str(image_id) + ".jpg")
        image = io.imread(img_name)
        image = transform.resize(image, (960, 540))
        
        label = self.dataset.iloc[idx, 2]

        x_min = self.dataset.iloc[idx, 5]
        y_min = self.dataset.iloc[idx, 6]
        x_max = self.dataset.iloc[idx, 7]
        y_max = self.dataset.iloc[idx, 8]
        
        sample = { 'image': image, 'image_id': image_id, 'object_id': object_id, 'label': int(label), 
                    'x_min': x_min, 'y_min': y_min, 'x_max': x_max, 'y_max': y_max }
        
        if self.transform:
            sample_out = self.transform(sample)

        # Comment this out if you don't want 200gb of tensors saved on your computer
        torch.save(sample_out, tensor_path)
        return sample_out

