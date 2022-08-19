import numpy as np
import PIL.Image
import matplotlib.pyplot as plt
import torch
from skimage import transform
from model import ResNet, Block
import os
import saliency.core as saliency
import math

resized_h = 540
resized_w = 960

class Heatmap:

    def __init__(self, model_path):
        self.model = self.model(model_path)

    def img_transformations(self, img):
        tensor_img = self.toTensor(img)
        float_tensor = tensor_img.type(torch.FloatTensor)
        return float_tensor.requires_grad_(True)

    def toTensor(self, maskImg):
        transpose_img = maskImg.transpose((0,3,1,2))
        return torch.from_numpy(transpose_img)

    def model(self, model_path):
        model = ResNet(18, Block, 4, 2)
        model.load_state_dict(torch.load(os.getcwd() + model_path, map_location=torch.device('cpu')))
        model.eval()
        return model
    
    def call_model_function(self, images,call_model_args=None, expected_keys=None):
        images = self.img_transformations(images)
        target_class_idx =  call_model_args['class_idx_str']
        output = self.model(images)
        m = torch.nn.Softmax(dim=1)
        output = m(output)
        if saliency.base.INPUT_OUTPUT_GRADIENTS in expected_keys:
            print("gradients")
            outputs = output[:,target_class_idx]
            grads = torch.autograd.grad(outputs, images, grad_outputs=torch.ones_like(outputs))
            grads = torch.movedim(grads[0], 1, 3)
            gradients = grads.detach().numpy()
            return {saliency.base.INPUT_OUTPUT_GRADIENTS: gradients}

    def loadImage(self, img_path, bounds):
        im = PIL.Image.open(os.getcwd() + img_path)
        im = np.asarray(im)
        img_resize = transform.resize(im, (960, 540))
        im_mask = self.applyMask(im, img_resize, bounds)
        return im_mask

    def applyMask(self, img, img_resize, bounds):
        binary_mask = np.zeros(shape=(img_resize.shape[0], img_resize.shape[1]))

        x_min = math.floor((bounds[0]/img.shape[0])*resized_w)
        y_min = math.floor((bounds[1]/img.shape[1])*resized_h)
        x_max = math.floor((bounds[2]/img.shape[0])*resized_w)
        y_max = math.floor((bounds[3]/img.shape[1])*resized_h)
            
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                    binary_mask[y,x] = 1 #sets binary mask value to 1 if within tappable bounds

        concat = np.dstack((img_resize, binary_mask)) #matrix multiplication of image and binary mask
        return concat

    def createSegments(self, object_array, img):
        segments = []
        for bounds in object_array:
            width = img.shape[0]
            height = img.shape[1]
            binary_mask = np.zeros(shape=(960, 540))
            x_ratio_min = bounds[0]/width
            x_ratio_max = bounds[2]/width
            y_ratio_min = bounds[1]/height
            y_ratio_max = bounds[3]/height

            for x in range(960):
                for y in range(540):
                    if x_ratio_min <= x/width < x_ratio_max and y_ratio_min <= y/height < y_ratio_max:
                        binary_mask[x,y] = 1
        segments.append(binary_mask)
        return segments

    def createHeatmap(self, img_path,pred, bounds, object_array=None):
        call_model_args = {'class_idx_str': pred,
                    'object_bounds': bounds}
        im_orig = self.loadImage(img_path, bounds)
        im = im_orig.astype(np.float32)
        if object_array:
            segments = self.createSegments(object_array, im_orig)
        else:
            segments = None
        xrai_object = saliency.XRAI()
        xrai_attributions = xrai_object.GetMask(im, self.call_model_function, call_model_args, batch_size=20, segments =segments)
        self.showHeatMap(xrai_attributions, title='XRAI Heatmap')

    def showHeatMap(self, im, title):
        plt.figure(2)
        plot = plt.imshow(im, cmap='RdBu')
        plt.colorbar(plot, orientation="vertical")
        plt.title(title)
        plt.show()