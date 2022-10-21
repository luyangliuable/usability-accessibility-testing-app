import numpy as np
import PIL.Image
import matplotlib.pyplot as plt
import torch
from skimage import transform
import os
import saliency.core as saliency
import math

RESIZE_WIDTH = 540
RESIZE_HEIGHT = 960

class Heatmap:

    def __init__(self, img_path, model, output_path):
        self.img_path = img_path
        self.model = model
        self.bounds = []
        self.out_path = output_path

    def createHeatmap(self, object_bounds, prediction, id):
        call_model_args = {'class_idx_str': prediction,
                    'object_bounds': object_bounds}
        im_orig = self.loadImage(self.img_path, object_bounds)
        im = im_orig.astype(np.float32)
        xrai_object = saliency.XRAI()
        print("creating heatmap")
        xrai_attributions = xrai_object.GetMask(im, self.call_model_function, call_model_args, batch_size=20, segments =None)
        return self.storeHeatMap(xrai_attributions,id)

    def img_transformations(self, img):
        tensor_img = self.toTensor(img)
        float_tensor = tensor_img.type(torch.FloatTensor)
        return float_tensor.requires_grad_(True)

    def toTensor(self, maskImg):
        transpose_img = maskImg.transpose((0,3,1,2))
        return torch.from_numpy(transpose_img)
    
    def call_model_function(self, images,call_model_args=None, expected_keys=None):
        images = self.img_transformations(images)
        target_class_idx =  call_model_args['class_idx_str']
        output = self.model(images)
        m = torch.nn.Softmax(dim=1)
        output = m(output)
        if saliency.base.INPUT_OUTPUT_GRADIENTS in expected_keys:
            outputs = output[:,target_class_idx]
            grads = torch.autograd.grad(outputs, images, grad_outputs=torch.ones_like(outputs))
            grads = torch.movedim(grads[0], 1, 3)
            gradients = grads.cpu().detach().numpy()
            return {saliency.base.INPUT_OUTPUT_GRADIENTS: gradients}

    def loadImage(self, img_path, bounds):
        im = PIL.Image.open(img_path)
        im = np.asarray(im)
        img_resize = transform.resize(im, (RESIZE_HEIGHT, RESIZE_WIDTH))
        im_mask = self.applyMask(img_resize, bounds, im.shape[0], im.shape[1])
        return im_mask

    def applyMask(self, img_resize, bounds, height, width):
        binary_mask = np.zeros(shape=(img_resize.shape[0], img_resize.shape[1]))

        x_min = math.floor((bounds[0]/width)*img_resize.shape[1])
        x_max = math.floor((bounds[2]/width)*img_resize.shape[1])
        y_min = math.floor((bounds[1]/height)*img_resize.shape[0])
        y_max = math.floor((bounds[3]/height)*img_resize.shape[0])

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                    binary_mask[y,x] = 1 #sets binary mask value to 1 if within tappable bounds

        concat = np.dstack((img_resize, binary_mask)) #matrix multiplication of image and binary mask
        return concat
        
    def storeHeatMap(self, xrai, id):
        plt.figure()
        im = PIL.Image.open(self.img_path)
        im = np.asarray(im)
        img_resize = transform.resize(im, (RESIZE_HEIGHT, RESIZE_WIDTH))
        plot = plt.imshow(img_resize)
        plot = plt.imshow(xrai, cmap='Reds', alpha=0.6)
        plt.colorbar(plot, orientation="vertical")
        name = 'heatmap_' + str(id) + '.jpg'
        path = os.path.join(self.out_path, name)
        plt.savefig(path)
        return path