from email.mime import image
import os
from heatmap import Heatmap
from dataset import Tappable
from torch.utils.data import DataLoader
from model import ResNet, Block
import torch
from torchvision.utils import draw_bounding_boxes
from torchvision.io import read_image
import matplotlib.pyplot as plt
import torchvision
import json
import sys
import getopt
import torch.nn as nn
import numpy as np
import math
import skimage.draw as skdraw
import skimage.io as io

MODEL_PATH = os.path.join(os.getcwd(), "trained_models/resnet_v3.pt")
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(DEVICE)

def get_bound_masks(img_path, json_path) -> list:
    # get original image dimensions
    image = io.imread(img_path)
    width = image.shape[1]
    height = image.shape[0]
    
    # get bounds of all views
    all_bounds = []
    json_file = open(json_path).read()
    json_data = json.loads(json_file)
    for view in json_data['views']:
        if view['visible'] and view['child_count'] == 0:
            bounds_out = view['bounds']
            bounds_item = [
                math.floor(int(bounds_out[0][0])/width)*540, 
                math.floor(int(bounds_out[0][1])/height)*960, 
                math.floor(int(bounds_out[1][0])/width)*540, 
                math.floor(int(bounds_out[1][1])/height)*960
                ]
            all_bounds.append(bounds_item)

    segments = []
    for item in all_bounds:
        # xmin, ymin, xmax, ymax
        rec = skdraw.rectangle(start=(item[1], item[0]), end=(item[3], item[2]),
                            shape=(960, 540))
        seg = np.zeros(shape=(960, 540), dtype=bool)
        seg[tuple(rec)] = True
        segments.append(seg) 
    return segments if len(segments) > 0 else None
    

def pipeline(img_path, json_path, output_path, threshold):
    bounds = []
    colours = []

    json_file = open(json_path).read()
    json_data = json.loads(json_file)
    for view in json_data['views']:
        if view['clickable'] == True: 
            bounds_out = view['bounds']
            bounds_item = [int(bounds_out[0][0]), int(bounds_out[0][1]), int(bounds_out[1][0]), int(bounds_out[1][1])]
            bounds.append(bounds_item)

    #Create dataset and dataloader 
    dataset = Tappable(img_path = img_path, bounds = bounds)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    #Create model from saved state
    model = ResNet(18, Block, 4, 2)
    model.to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device(DEVICE)))
    if DEVICE == 'cuda':
        model = nn.DataParallel(model)
    model.eval()

    json_out = {}
    bounding_boxes_all = []
    counter = 0
    labels = ["tappable", "not tappable"]

    #Create heatmap
    # segments = get_bound_masks(img_path, json_path)
    segments = None
    heatmap = Heatmap(img_path, model, output_path, bounds=segments)

    #Run model on dataset 
    for batch_idx, item in enumerate(dataloader):
        if DEVICE == 'cuda':
            outputs = model(item['image'].type(torch.cuda.FloatTensor))
        else:
            outputs = model(item['image'].type(torch.FloatTensor))
        _, indices = torch.sort(outputs, descending=True)
        percentage = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
        _, index = torch.max(outputs, 1) 
        print([(labels[idx], percentage[idx].item()) for idx in indices[0][:2]])
        bounding_boxes = []
        bounding_boxes_all.append(item['bounds'])
        for i in range(len(item['bounds'])):
            if isinstance(item['bounds'][i], torch.Tensor):
                bounding_boxes.append(item['bounds'][i].to(device='cpu', non_blocking=True).item())
            else:
                bounding_boxes.append(item['bounds'][i])

        if index[0] == 1 and percentage[index[0]].item()>=threshold:
            colours.append("red")
            heatmap_path = heatmap.createHeatmap(item['bounds'], index[0], counter)
        else:
            # colours.append("black")
            # heatmap_path = None
            colours.append("red")
            heatmap_path = heatmap.createHeatmap(item['bounds'], index[0], counter)
            
        details_out = {'bounds': bounding_boxes, 'percentage': percentage[index[0]].item(), 'heatmap': heatmap_path}
        json_out[str(counter)] = details_out
        counter += 1

    #Store bounding boxes for those rated untappable
    if bounding_boxes_all:
        img = read_image(img_path)
        boxes = torch.tensor(bounding_boxes_all, dtype=torch.float)
        result = draw_bounding_boxes(img, boxes, width=8, colors=colours)
        img = torchvision.transforms.ToPILImage()(result)
        img.save(os.path.join(output_path, 'screenshot.jpg'))

    #Save json file 
    with open(os.path.join(output_path, 'description.json'), 'w+') as file:
        json.dump(json_out, file)


def run_pipeline(img_dir, json_dir, output_dir, threshold):
    for image in os.listdir(img_dir):
        if image[-4:] != '.jpg':
            continue
        img_name = image.split('.jpg')[0]
        img_path = os.path.join(img_dir, image)
        json_path = os.path.join(json_dir, img_name + '.json')
        if os.path.exists(json_path):
            output_path = os.path.join(output_dir, img_name)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            pipeline(img_path , json_path, output_path, threshold)

if __name__=='__main__':
    args = sys.argv[1:]
    options, args = getopt.getopt(args, "i:j:o:t:",
                               ["image_dir =",
                                "json_dir =",
                                "output_dir =",
                                "threshold ="])
    for name, value in options:
        if name in ['-i', '--image_dir']:
            image_dir = value
        elif name in ['-j', '--json_dir']:
            json_dir = value
        elif name in ['-o', '--output_dir']:
            output_dir = value
        elif name in ['-t', '--threshold']:
            threshold = int(value)
    run_pipeline(image_dir, json_dir, output_dir, threshold)
