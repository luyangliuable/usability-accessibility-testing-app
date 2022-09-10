import re
import json
import xmltodict

def update_list(json_children):
    """
    Loops through list of children and calls update on individual dictionary
    """
    out = []
    for child in json_children:
        child_out = update_dict(child)
        out.append(child_out)
    return out


def update_dict(child):
    """
    Updates json file for dictionary item and children. Renames keys, change type of values and format null. 
    """
    if "node" not in child:
        child["child_count"] = 0
    children_copy = child.copy()
    for key, val in children_copy.items():
            if key == 'index':
                child[key] = int(val)
            elif key == "node":
                child["children"] = child.pop("node")
                if type(child["children"]) == list:
                    child["child_count"] = len(child["children"])
                else:
                    child["child_count"] = 1
                if child["child_count"] > 1:
                    child["children"] = update_list(child["children"])
                else:
                    child["children"] = update_dict(child["children"])
            elif key =="bounds":
                re_text = r"\[(\d*?),(\d*?)\]\[(\d*?),(\d*?)\]"
                bounds_out = re.findall(re_text, val)[0]
                bounds_json = [[int(bounds_out[0]), int(bounds_out[1])], [int(bounds_out[2]), int(bounds_out[3])]]
                child[key] = bounds_json
            elif key =="password":
                pw = bool(child.pop("password"))
                child["is_password"] = pw
            elif key =="long-clickable":
                lc = bool(child.pop("long-clickable"))
                child["long_clickable"] = lc
            elif val == "true" or val == "false":
                child[key] = bool(val)
            elif val == "":
                child[key] = None
    return child

def node_list(a, final, counter):
    if "children" in a:
        out = []
        if type(a["children"])==list:
            for child in a["children"]:
                final, counter= node_list(child.copy(), final.copy(), counter)
                out.append(counter)
                counter +=1
        else:
            final, counter= node_list(a["children"].copy(), final.copy(), counter)
            out.append(counter)
            counter +=1
        a["children"] = out.copy()
    final[counter] =a.copy()
    return final, counter


def convert_xml_to_json(xml_path, json_path):
    """
    Converts storydistiller xml file to json format
    """
    with open(xml_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read(),attr_prefix='')
        data_node = data_dict["hierarchy"]["node"]

    json_file_updated= update_dict(data_node)

    final = {}
    counter = 0
    json_node_out, _= node_list(json_file_updated, final, counter)

    views_out = {"views": json_node_out}

    json_str = json.dumps(views_out, indent=4)

    json_out = open(json_path, "w+")
    json_out.write(json_str)
    json_out.close()

if __name__=='__main__':
   convert_xml_to_json("/Users/em.ily/Downloads/a2dp.Vol.ManageData.xml", "data6.json")