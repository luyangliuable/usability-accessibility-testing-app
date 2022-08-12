import numpy as np
import torch
from configparser import ConfigParser
from skimage import io, transform
from model import ResNet, Block
from heatmap import Heatmap
import os
import matplotlib.pyplot as plt
import math
from PIL import Image

resized_h = 540
resized_w = 960

class ModelPipeline:

    def __init__(self, img_path, bounds, model):
        self.img_path = img_path
        self.img = self.getImage()
        self.bounds = bounds
        self.bounds_resize = self.updateArray(self.bounds)
        self.model_path = model
        self.prediction = None 

    #Gets stored image [TODO: update to get image from s3 bucket]
    def getImage(self):
        self.validateImage()
        return io.imread(os.getcwd() + self.img_path)

    def updateArray(self, bounds):
        for i in range(len(bounds)):
            bounds[i] = int(bounds[i])
        bounds = self.get_relative_bounds(bounds)
        return bounds

    def get_relative_bounds(self, obj_bounds):
        x_min = math.floor((obj_bounds[0]/self.img.shape[0])*resized_w)
        y_min = math.floor((obj_bounds[1]/self.img.shape[1])*resized_h)
        x_max = math.floor((obj_bounds[2]/self.img.shape[0])*resized_w)
        y_max = math.floor((obj_bounds[3]/self.img.shape[1])*resized_h)
        return [x_min, y_min, x_max, y_max]
            
    #Applies binary mask of button onto image matrix
    def applyMask(self, resizeImg):
        binary_mask = np.zeros(shape=(resizeImg.shape[0], resizeImg.shape[1]))

        x_min = self.bounds_resize[0]
        x_max = self.bounds_resize[2]
        y_min = self.bounds_resize[1]
        y_max = self.bounds_resize[3]
        
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                    binary_mask[y,x] = 1 #sets binary mask value to 1 if within tappable bounds

        concat = np.dstack((resizeImg, binary_mask)) #matrix multiplication of image and binary mask
        return concat

    #Converts image to tensor
    def toTensor(self, maskImg):
        transpose_img = maskImg.transpose((2, 0, 1))
        return torch.from_numpy(transpose_img)

    #Apply Transformations
    def image_transformations(self):
        img_resize = transform.resize(self.img, (960, 540))
        mask_img = self.applyMask(img_resize)
        tensor_img = self.toTensor(mask_img)
        tensor = tensor_img.unsqueeze(0)
        float_tensor = tensor.type(torch.FloatTensor)
        return float_tensor

    #Image validation
    def validateImage(self):
        if self.img_path[-3:] != 'jpg':
            raise Exception("File must be of type jpg")

    def modelPipeline(self):
        #Apply Image Transformations
        input = self.image_transformations()

        #Create model from saved state
        model = ResNet(18, Block, 4, 2)
        model.load_state_dict(torch.load(os.getcwd() + self.model_path, map_location=torch.device('cpu')))
        model.eval()

        #Prediction
        labels = ['tappable' ,'not tappable'] 
        with torch.no_grad():
            predictions = model(input)
            percentage = torch.nn.functional.softmax(predictions, dim=1)[0] * 100
            _, indices = torch.sort(predictions, descending=True)
            print([(labels[idx], percentage[idx].item()) for idx in indices[0][:5]])
            _, index = torch.max(predictions, 1) 
            return str(round(percentage[index[0]].item(),2)) + "%; rated " + labels[index[0]],index[0]

    def showImage(self, pred_str):
        fig = plt.figure()
        fig.suptitle(pred_str, fontsize=15)
        ax1 = fig.add_subplot(1,2,1)
        im = Image.open(os.getcwd() + self.img_path)
        ax1.imshow(im)
        ax2 = fig.add_subplot(1,2,2)
        im1 = im.crop(self.bounds)
        ax2.imshow(im1)
        ax1.title.set_text("Original Image")
        ax2.title.set_text("Cropped Image")
        plt.show()

if __name__ == '__main__':
    #Read config file
    config = ConfigParser()
    config.read('config.ini')

    #Get image path
    img_path = config.get('main', 'image')

    #Get object bounds
    bounds = config.get('main', 'bounds')
    bounds_array = bounds.strip('[]').split(',')

    #Get model
    model_path = config.get('main', 'model')

    #Get prediction
    prediction = ModelPipeline(img_path, bounds_array,model_path)
    prediction_str, pred_val = prediction.modelPipeline()
    prediction.showImage(prediction_str)

    #Heatmap
    heatmap = Heatmap(model_path)
    heatmap.createHeatmap(img_path,pred_val,bounds_array,object_array=None)