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
import sys

def pipeline(img_path, json_path, output_path):
    bounds = []
    colours = []


    json_file = open(json_path).read()
    json_data = json.loads(json_file)
    for view in json_data['views']:
        if view['clickable'] == True: 
            bounds_out = view['bounds']
            bounds_item = [int(bounds_out[0][0]), int(bounds_out[0][1]), int(bounds_out[1][0]), int(bounds_out[1][1])]
            bounds.append(bounds_item)
    
    # #Extract bounds and item details from xml file 
    # xml_file = open(xml_path).read()
    # regex_text = r"<node[\s\S]*?text=\"([\s\S]*?)\"[\s\S]*?class=\"([a-zA-z.]*?)\"[\s\S]*?clickable=\"([a-z]*)\"[\s\S]*?bounds=\"([\s\S]*?)\""
    # regex_out = re.findall(regex_text, xml_file)
    # for i in range(len(regex_out)):
    #     #Store xml output in json file 
    #     output[str(i)] = {"title": regex_out[i][0], "class": regex_out[i][1], "clickable": regex_out[i][2], "bounds": regex_out[i][3]}
    #     #Get bounds for clickable items
    #     if regex_out[i][2] == "true":
    #         re_text = r"\[(\d*?),(\d*?)\]\[(\d*?),(\d*?)\]"
    #         bounds_out = re.findall(re_text, regex_out[i][3])[0]
    #         bounds_item = [int(bounds_out[0]), int(bounds_out[1]), int(bounds_out[2]), int(bounds_out[3])]
    #         bounds.append(bounds_item)

    #Create dataset and dataloader 
    dataset = Tappable(img_path = img_path, bounds = bounds)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    #Create model from saved state
    model = ResNet(18, Block, 4, 2)
    model.load_state_dict(torch.load(os.getcwd() + "/trained_models/resnet_v3.pt", map_location=torch.device('cpu')))
    model.eval()

    json_out = {}
    bounding_boxes_all = []
    counter = 0
    labels = ["tappable", "not tappable"]

    #Create heatmap
    heatmap = Heatmap(img_path, model, output_path)

    #Run model on dataset 
    for batch_idx, item in enumerate(dataloader):
        outputs = model(item['image'].type(torch.FloatTensor))
        _, indices = torch.sort(outputs, descending=True)
        percentage = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
        _, index = torch.max(outputs, 1) 
        print([(labels[idx], percentage[idx].item()) for idx in indices[0][:2]])
        bounding_boxes = []
        bounding_boxes_all.append(item['bounds'])
        for i in range(len(item['bounds'])):
            if isinstance(item['bounds'][i], torch.Tensor):
                bounding_boxes.append(item['bounds'][i].cpu().item())
            else:
                bounding_boxes.append(item['bounds'][i])

        if int(index[0]) == 1:
            colours.append("red")
            heatmap_path = heatmap.createHeatmap(item['bounds'], index[0], counter)
        else:
            colours.append("black")
            heatmap_path = None
            
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


def run_pipeline(img_dir, json_dir, output_dir):
    for images in os.listdir(img_dir):
        img_path = img_dir + images
        img_name = images.strip('.jpg').strip('screen')
        json_path = json_dir + 'state' + img_name + '.json'
        if os.path.exists(json_path):
            output_path = output_dir + img_name + "/"
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            pipeline(img_path , json_path, output_path)

if __name__=='__main__':
    args = sys.argv[1:]
    if len(args) == 3:
        run_pipeline(args[0], args[1], args[2])