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

#TODO - get image from storage + object_bounds (clickable & all) from xrai json file
# object_bounds = [[789,1177,1038,1454],[291,1496,540,1773],[765,1030,1069,1156],[291,1177,540,1454],[540,1177,789,1454],[42,1020,765,1132]]
# path = "/Users/em.ily/Documents/GitHub/FIT3170_Usability_Accessibility_Testing_App/pipeline/test_image/17380.jpg"

# object_bounds = [[52,875,1027,980],[827,441,937,519],[758,1108,880,1230],[52,730,1027,835],[880,1108,1002,1230]]
# path = "/Users/em.ily/Documents/GitHub/FIT3170_Usability_Accessibility_Testing_App/pipeline/test_image/34354.jpg"

object_bounds = [[975,73,1080,199],[709,486,1038,605],[614,423,851,486],[42,1562,1038,1649],[42,513,303,577],[42,236,1038,362]]
path = "/Users/em.ily/Documents/GitHub/FIT3170_Usability_Accessibility_Testing_App/pipeline/test_image/59175.jpg"

file, extention = os.path.splitext(path)
if not os.path.exists(file + "/"):
    os.makedirs(file)

#Create dataset and dataloader 
dataset = Tappable(img_path = path, bounds = object_bounds)
dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

#Create model from saved state
model = ResNet(18, Block, 4, 2)
model.load_state_dict(torch.load(os.getcwd() + "/trained_models/resnet_v3.pt", map_location=torch.device('cpu')))
model.eval()

untappable_bounds = {}
bounding_boxes_all = []
counter = 0
labels = ["tappable", "not tappable"]

#Create heatmap
heatmap = Heatmap(path, model, file, segments=None)

#Run model on dataset 
for batch_idx, item in enumerate(dataloader):
    outputs = model(item['image'].type(torch.FloatTensor))
    _, indices = torch.sort(outputs, descending=True)
    percentage = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
    _, index = torch.max(outputs, 1) 
    print([(labels[idx], percentage[idx].item()) for idx in indices[0][:2]])

    if int(index[0]) == 1:
        bounding_boxes = []
        bounding_boxes_all.append(item['bounds'])
        for i in range(len(item['bounds'])):
            if isinstance(item['bounds'][i], torch.Tensor):
                bounding_boxes.append(item['bounds'][i].cpu().item())
            else:
                bounding_boxes.append(item['bounds'][i])
        heatmap_path = heatmap.createHeatmap(item['bounds'], index[0], counter)
        untappable = {'bounds': bounding_boxes, 'percentage': percentage[index[0]].item(), 'heatmap': heatmap_path}
        untappable_bounds[str(counter)] = untappable
        counter += 1

#Store bounding boxes for those rated untappable
if bounding_boxes_all:
    img = read_image(path)
    boxes = torch.tensor(bounding_boxes_all, dtype=torch.float)
    result = draw_bounding_boxes(img, boxes, width=8)
    img = torchvision.transforms.ToPILImage()(result)
    img.save(os.path.join(file, 'bounding_box.jpg'))

#Save json file 
with open(os.path.join(file, 'details.json'), 'w+') as file:
    json.dump(untappable_bounds, file)

