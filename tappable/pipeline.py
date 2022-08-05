import numpy as np
import torch
from configparser import ConfigParser
from skimage import io, transform
from model import ResNet, Block
import os

#Applies binary mask of button onto image matrix
def applyMask(img, object_bounds):
    width = img.shape[0]
    height = img.shape[1]

    binary_mask = np.zeros(shape=(width, height))
    x_ratio_min = object_bounds[0]/width
    x_ratio_max = object_bounds[2]/width
    y_ratio_min = object_bounds[1]/height
    y_ratio_max = object_bounds[3]/height
        
    for x in range(width):
        for y in range(height):
            if x_ratio_min <= x/width < x_ratio_max and y_ratio_min <= y/height < y_ratio_max:
                binary_mask[x,y] = 1 
    concat = np.dstack((img, binary_mask)) 
    return concat

#Converts image to tensor
def toTensor(img):
    transpose_img = img.transpose((2, 0, 1))
    return torch.from_numpy(transpose_img)

#Apply Transformations
def image_transformations(img, bounds):
    image = transform.resize(img, (960, 540))
    mask_img = applyMask(image, bounds)
    tensor_img = toTensor(mask_img)
    tensor = tensor_img.unsqueeze(0)
    input = tensor.type(torch.FloatTensor)
    return input

#Get image path
config = ConfigParser()
config.read('config.ini')
img_path = config.get('main', 'image')
img = io.imread(os.getcwd() + img_path) #TODO: Change to accept uploaded image

#Get object bounds
bounds = config.get('main', 'bounds')
bounds = [0,2217, 0, 2392] #clickable 

#Apply transformations to image
input = image_transformations(img, bounds)

#Create model from saved state
model = ResNet(18, Block, 4, 1000)
model.load_state_dict(torch.load('resnet.pt', map_location=torch.device('cpu')))
model.eval()

#Prediction
labels = ['0' ,'1', '2', '3', '4', '5'] 
with torch.no_grad():
    predictions = model(input)
    _, index = torch.max(predictions, 1)
    percentage = torch.nn.functional.softmax(predictions, dim=1)[0] * 100
    print(str(round(percentage[index[0]].item(),2)) + "%; rated " + labels[index[0]] + "/5 tappable")
