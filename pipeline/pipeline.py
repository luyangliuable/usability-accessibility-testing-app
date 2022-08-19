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
import re

output = {}
bounds = []

xml_file = open(r"/Users/em.ily/Downloads/a2dp.Vol.ManageData.xml").read() #TODO: XML FILE FROM XBOT

#Extract bounds and item details from xml file 
regex_text = r"<node[\s\S]*?text=\"([\s\S]*?)\"[\s\S]*?class=\"([a-zA-z.]*?)\"[\s\S]*?clickable=\"([a-z]*)\"[\s\S]*?bounds=\"([\s\S]*?)\""
regex_out = re.findall(regex_text, xml_file)
for i in range(len(regex_out)):
    #Store xml output in json file 
    output[str(i)] = {"title": regex_out[i][0], "class": regex_out[i][1], "clickable": regex_out[i][2], "bounds": regex_out[i][3]}
    #Get bounds for clickable items
    if regex_out[i][2] == "true":
        re_text = r"\[(\d*?),(\d*?)\]\[(\d*?),(\d*?)\]"
        bounds_out = re.findall(re_text, regex_out[i][3])[0]
        bounds_item = [int(bounds_out[0]), int(bounds_out[1]), int(bounds_out[2]), int(bounds_out[3])]
        bounds.append(bounds_item)

path = "/Users/em.ily/Documents/GitHub/FIT3170_Usability_Accessibility_Testing_App/pipeline/test_image/unknown.jpg" #TODO: PATH TO IMAGE FILE

#Create directory 
file, extention = os.path.splitext(path)
if not os.path.exists(file + "/"):
    os.makedirs(file)

#Store xml details as json (can comment out if not needed)
json_out = json.dumps(output)
file_out = open(os.path.join(file, 'xml_json_out.json'), 'w+')
file_out.write(json_out)

#Create dataset and dataloader 
dataset = Tappable(img_path = path, bounds = bounds)
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
heatmap = Heatmap(path, model, file) #TODO: Change segments = bounds_all to run with object bounds

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

