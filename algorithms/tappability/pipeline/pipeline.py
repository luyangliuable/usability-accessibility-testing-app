import numpy as np
import torch
from configparser import ConfigParser
from skimage import io, transform
from model import ResNet, Block
from heatmap import Heatmap
import os
import matplotlib.pyplot as plt

class ModelPipeline:

    def __init__(self, img_path, bounds, model):
        self.img_path = img_path
        self.bounds = self.updateArray(bounds)
        self.img = self.getImage()
        self.model_path = model
        self.prediction = None 

    #Gets stored image [TODO: update to get image from s3 bucket]
    def getImage(self):
        self.validateImage()
        return io.imread(os.getcwd() + self.img_path)

    def updateArray(self, bounds):
        for i in range(len(bounds)):
            bounds[i] = int(bounds[i])
        return bounds
            
    #Applies binary mask of button onto image matrix
    def applyMask(self, resizeImg):
        width = resizeImg.shape[0]
        height = resizeImg.shape[1]

        binary_mask = np.zeros(shape=(width, height))
        x_ratio_min = self.bounds[0]/width
        x_ratio_max = self.bounds[2]/width
        y_ratio_min = self.bounds[1]/height
        y_ratio_max = self.bounds[3]/height
            
        for x in range(width):
            for y in range(height):
                if x_ratio_min <= x/width < x_ratio_max and y_ratio_min <= y/height < y_ratio_max:
                    binary_mask[x,y] = 1 
        concat = np.dstack((resizeImg, binary_mask)) 
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
        ax1.imshow(self.img)
        ax2 = fig.add_subplot(1,2,2)
        cropped = self.img[self.bounds[1]:self.bounds[3], self.bounds[0]:self.bounds[2]]
        ax2.imshow(cropped)
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

    prediction = ModelPipeline(img_path, bounds_array,model_path)
    prediction_str, pred_val = prediction.modelPipeline()
    prediction.showImage(prediction_str)

    #Heatmap
    heatmap = Heatmap(model_path)
    heatmap.createHeatmap(img_path,pred_val,bounds_array,object_array=None)