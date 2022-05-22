import argparse
import cv2
import numpy as np
import torch
from torch.autograd import Function, Variable
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from network import Net
import torch.nn as nn
import getdata
import os
# import matplotlib.pyplot as plt
import requests

raw_dir = './png_pic/'
image_dir = './input_pic/'
model_dir = './model/4model.pth'

class FeatureExtractor():
    """ Class for extracting activations and
    registering gradients from targetted intermediate layers """

    def __init__(self, model, target_layers):
        self.model = model
        self.target_layers = target_layers
        self.gradients = []

    def save_gradient(self, grad):
        self.gradients.append(grad)

    def __call__(self, x):
        outputs = []
        self.gradients = []

        for name, module in self.model.module.features._modules.items():
            x = module(x)
            if name in self.target_layers:
                x.register_hook(self.save_gradient)
                outputs += [x]
        return outputs, x


class ModelOutputs():
    """ Class for making a forward pass, and getting:
    1. The network output.
    2. Activations from intermeddiate targetted layers.
    3. Gradients from intermeddiate targetted layers. """

    def __init__(self, model, target_layers):
        self.model = model
        self.feature_extractor = FeatureExtractor(self.model, target_layers)

    def get_gradients(self):
        return self.feature_extractor.gradients

    def __call__(self, x):
        target_activations, output = self.feature_extractor(x)
        output = output.view(output.size(0), -1)

        return target_activations, output


def preprocess_image(image_file):


    imgs_data = [] 
    img = Image.open(image_file)  
    img_data = getdata.dataTransform(img)  

    imgs_data.append(img_data)  
    imgs_data = torch.stack(imgs_data)  
    input = Variable(imgs_data, requires_grad = True)
    return input


def show_cam_on_image(img, mask,image_num):
    # Formely localization_result: writes resulting image to output_pic
    heatmap = cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET)
    heatmap = np.float32(heatmap) / 255
    cam = heatmap + np.float32(img)
    cam = cam / np.max(cam)
    cv2.imwrite("./output_pic/{0}cam.jpg".format(image_num), np.uint8(255 * cam))

    # txtpath = './outputtxt2/{0}.txt'.format(image_num)
    # IMGpath = './examples/{0}.jpg'.format(image_num)
    # im = Image.open(IMGpath)
    # print(im.size[0])
    # x_num = im.size[0] / 448
    # y_num = im.size[1] / 768

    # gray = cv2.cvtColor(cam,cv2.COLOR_BGR2GRAY)
    # image = gray * 255
    # ret, thresh = cv2.threshold(image, 230, 255, cv2.THRESH_BINARY)
    # cv2.imwrite("0.jpg",thresh)
    # thresh = cv2.imread("0.jpg",cv2.IMREAD_GRAYSCALE)
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    #
    # for i in range(0, len(contours)):
    #     x, y, w, h = cv2.boundingRect(contours[i])
    #     if w<10 or h <10:
    #         nnnnn =1
    #     else:
    #         cv2.rectangle(img, (x, y), (x + w, y + h), (153, 153, 0), 1)
    #
    #         xmin = x * x_num
    #         ymin = y * y_num
    #         xmax = (x + w) * x_num
    #         ymax = (y + h) * y_num
    #         with open(txtpath, "a") as ms:
    #             ms.write("component occlusion" + "\n")
    #             ms.write(str(int(xmin)) + "\n")
    #             ms.write(str(int(ymin)) + "\n")
    #             ms.write(str(int(xmax)) + "\n")
    #             ms.write(str(int(ymax)) + "\n")
    #
    #
    # cv2.imshow("gray1", img)
    # cv2.waitKey(0)
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
    # cv2.imshow("gray1", img)
    # cv2.waitKey(0)
 

class GradCam:
    def __init__(self, model, target_layer_names, use_cuda):
        self.model = model
        self.model.eval()
        self.cuda = use_cuda
        if self.cuda:
            self.model = model.cuda()

        self.extractor = ModelOutputs(self.model, target_layer_names)

    def forward(self, input):
        return self.model(input)

    def __call__(self, input, index=None):
        if self.cuda:
            features, output = self.extractor(input.cuda())
        else:
            features, output = self.extractor(input)

        if index == None:
            index = np.argmax(output.cpu().data.numpy())

        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0][index] = 1
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)
        if self.cuda:
            one_hot = torch.sum(one_hot.cuda() * output)
        else:
            one_hot = torch.sum(one_hot * output)

        self.model.zero_grad()
        one_hot.backward(retain_graph=True)

        grads_val = self.extractor.get_gradients()[-1].cpu().data.numpy()

        target = features[-1]
        target = target.cpu().data.numpy()[0, :]

        weights = np.mean(grads_val, axis=(2, 3))[0, :]
        cam = np.zeros(target.shape[1:], dtype=np.float32)

        for i, w in enumerate(weights):
            cam += w * target[i, :, :]

        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (448, 768))
        cam = cam - np.min(cam)
        cam = cam / np.max(cam)
        return cam


class GuidedBackpropReLU(Function):

    @staticmethod
    def forward(self, input):
        positive_mask = (input > 0).type_as(input)
        output = torch.addcmul(torch.zeros(input.size()).type_as(input), input, positive_mask)
        self.save_for_backward(input, output)
        return output

    @staticmethod
    def backward(self, grad_output):
        input, output = self.saved_tensors
        grad_input = None

        positive_mask_1 = (input > 0).type_as(grad_output)
        positive_mask_2 = (grad_output > 0).type_as(grad_output)
        grad_input = torch.addcmul(torch.zeros(input.size()).type_as(input),
                                   torch.addcmul(torch.zeros(input.size()).type_as(input), grad_output,
                                                 positive_mask_1), positive_mask_2)

        return grad_input


class GuidedBackpropReLUModel:
    def __init__(self, model, use_cuda):
        self.model = model
        self.model.eval()
        self.cuda = use_cuda
        if self.cuda:
            self.model = model.cuda()

        for idx, module in self.model.module.features._modules.items():
            if module.__class__.__name__ == 'ReLU':
                self.model.module.features._modules[idx] = GuidedBackpropReLU.apply

    def forward(self, input):
        res=self.model.module(input)
        print(res)
        print('forward get res')
        return res


    def __call__(self, input, index=None):
        if self.cuda:
            output = self.forward(input.cuda())
        else:
            output = self.forward(input)

        if index == None:
            index = np.argmax(output.cpu().data.numpy())

        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0][index] = 1
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)
        if self.cuda:
            one_hot = torch.sum(one_hot.cuda() * output)
        else:
            one_hot = torch.sum(one_hot * output)

        one_hot.backward(retain_graph=True)
        output = input.grad.cpu().data.numpy()
        output = output[0, :, :, :]

        return output


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-cuda', action='store_true', default=False,
                        help='Use NVIDIA GPU acceleration') # https://docs.python.org/3/library/argparse.html#action
    parser.add_argument('--image-path', type=str,help='Input image path') # default='./examples/211.jpg',
                        
    args = parser.parse_args()
    args.use_cuda = args.use_cuda and torch.cuda.is_available()
    if args.use_cuda:
        print("Using GPU for acceleration")
    else:
        print("Using CPU for computation")

    return args

def deprocess_image(img):
    """ see https://github.com/jacobgil/keras-grad-cam/blob/master/grad-cam.py#L65 """
    img = img - np.mean(img)
    img = img / (np.std(img) + 1e-5)
    img = img * 0.1
    img = img + 0.5
    img = np.clip(img, 0, 1)
    return np.uint8(img*255)

def process_png_to_jpg():
    """
    Using PIL converts images from png to jpg
    """
    raw_pics = os.listdir(raw_dir)
    for raw_png in raw_pics:
        # print(raw_png)
        (filename, extension) = os.path.splitext(raw_png)
        if extension != ".txt":
            raw_png_dir = raw_dir + raw_png
            pil_jpg = Image.open(raw_png_dir, mode='r')

            pil_jpg__dir = image_dir + filename+".jpg"
            pil_jpg.convert('RGB').save(pil_jpg__dir,'JPEG')
    print("Files Converted from .png to .jpg")


if __name__ == '__main__':
    """ python grad_cam.py <path_to_image>
    1. Loads an image with opencv.
    2. Preprocesses it for VGG19 and converts to a pytorch variable.
    3. Makes a forward pass to find the category index with the highest score,
    and computes intermediate activations.
    4.Makes the visualization. 
    5. Uploads to redis
    """
    process_png_to_jpg()

    files = os.listdir(image_dir)

    for file in files:
        print(file)
        (filename, extension) = os.path.splitext(file)
        if extension != ".txt":
            image_num = filename
            image_name = image_dir + file
            print(image_name)
            args = get_args()

            model = Net()
            # model.cuda()
            model = nn.DataParallel(model)
            # model.load_state_dict(torch.load(model_dir))
            model.load_state_dict(torch.load(model_dir,map_location=torch.device('cpu'))) 

            grad_cam = GradCam(model=model, target_layer_names=["40"], use_cuda=args.use_cuda)
            img = cv2.imread(image_name, 1)
            img = np.float32(cv2.resize(img, (448, 768))) /255

            input = preprocess_image(image_name)
            target_index = None
            mask = grad_cam(input, target_index)
            show_cam_on_image(img, mask, image_num)

            # Extra: ???
            gb_model = GuidedBackpropReLUModel(model=model, use_cuda=args.use_cuda)
            gb = gb_model(input, index=target_index)

            gb = gb.transpose((1, 2, 0))

            cam_mask = cv2.merge([mask, mask, mask])
            cam_gb = deprocess_image(cam_mask*gb)
            gb = deprocess_image(gb)

            # cv2.imwrite('./output_pic_2/{0}gb.jpg'.format(image_num), gb)
            # cv2.imwrite('./output_pic_2/{0}cam_gb.jpg'.format(image_num), cam_gb)