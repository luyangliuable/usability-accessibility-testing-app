import numpy as np
import torch
from torch.utils.data import Dataset
from skimage import io, transform
from torchvision import transforms
import math

# Image tranformation
class applyMask(object):

    """
    Matrix multiplication of the RGB image and a binary mask of the object
    """

    def __call__(self, sample):
        
        image = sample['image']
        
        binary_mask = np.zeros(shape=(image.shape[0], image.shape[1]))
        x_min = math.floor((sample['x_min']/sample['width'])*image.shape[1])
        x_max = math.floor((sample['x_max']/sample['width'])*image.shape[1])
        y_min = math.floor((sample['y_min']/sample['height'])*image.shape[0])
        y_max = math.floor((sample['y_max']/sample['height'])*image.shape[0])
        
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                    binary_mask[y,x] = 1 #sets binary mask value to 1 if within tappable bounds

        concat = np.dstack((image, binary_mask)) #matrix multiplication of image and binary mask

        bounds = [sample['x_min'], sample['y_min'], sample['x_max'], sample['y_max']]
    
        return {'image': concat, 'bounds':bounds}


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        img = sample['image']
        # swap color axis because
        # numpy image: H x W x C
        # torch image: C x H x W
        image = img.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image), 'bounds': sample['bounds']}

dataTransform = transforms.Compose([applyMask(), ToTensor()])

class Tappable(Dataset):
    """
    Creates dataset from the csv of labelled image and object ids

    """

    def __init__(self, img_path, bounds):
        self.transform = dataTransform
        self.dataset = bounds
        self.img_path = img_path

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        image = io.imread(self.img_path)
        width = image.shape[1]
        height = image.shape[0]
        image = transform.resize(image, (960, 540))

        x_min = self.dataset[idx][0]
        y_min = self.dataset[idx][1]
        x_max = self.dataset[idx][2]
        y_max = self.dataset[idx][3]
        
        sample = { 'image': image,
                    'x_min': x_min, 'y_min': y_min, 'x_max': x_max, 'y_max': y_max,
                    'width': width, 'height': height}
        
        if self.transform:
            sample_out = self.transform(sample)

        return sample_out