import os
import pandas as pd
import json
import csv
import math

BASE_DATASET = pd.read_csv('https://raw.githubusercontent.com/google-research-datasets/taperception/main/rico_tap_annotations_idsonly.csv')
IMAGE_H = 2560
IMAGE_W = 1440

root_path = os.path.dirname(__file__)
json_dir = os.path.join(root_path, 'json_dir/')
dataset_path = os.path.join(root_path, 'dataset/tappability_dataset.csv')

resized_h = 960
resized_w = 540


def _get_obj_bounds(obj_id, json_obj):

    # if the json is object
    if 'pointer' in json_obj and json_obj['pointer']==obj_id:
        return json_obj['bounds']
    
    # check nested jsons recursively
    if 'children' in json_obj:
        for child in json_obj['children']:
            obj_bounds = _get_obj_bounds(obj_id, child)
            if obj_bounds is not None:
                return obj_bounds
    
    return None


def _get_relative_bounds(obj_bounds):
    x_min = math.floor((obj_bounds[0]/IMAGE_W)*resized_w)
    y_min = math.floor((obj_bounds[1]/IMAGE_H)*resized_h)
    x_max = math.floor((obj_bounds[2]/IMAGE_W)*resized_w)
    y_max = math.floor((obj_bounds[3]/IMAGE_H)*resized_h)
    
    return [x_min, y_min, x_max, y_max]


def get_data(idx):
    
    # get original data for index
    data = list(BASE_DATASET.iloc[idx].values)
    img_id = data[0]
    obj_id = data[1]
    
    # get root json
    json_root = json.load(open(json_dir + str(img_id) + '.json'))['activity']['root']

    # get obj bounds
    obj_bounds = _get_obj_bounds(obj_id, json_root)
    
    # get relative bounds (960x540)
    rel_bounds = _get_relative_bounds(obj_bounds)

    data.extend(rel_bounds)
    return data


def create_dataset():

    # create csv file and add header
    with open(dataset_path, 'w', newline='') as dataset_file:
        writer = csv.writer(dataset_file)
        header = ['img_id', 'object_id', 'label', 'raters_marked_tappable', 'split', 'x_min', 'y_min', 'x_max', 'y_max']
        
        writer.writerow(header)
    
    # write each row to csv
    for idx in range(len(BASE_DATASET)):
        data = get_data(idx)

        with open(dataset_path, 'a', newline='') as dataset_file:
            writer = csv.writer(dataset_file)
            writer.writerow(data)

        
if __name__=='__main__':
    create_dataset()
