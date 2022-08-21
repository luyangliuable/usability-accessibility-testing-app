import os
import sys

def file_order_sorter(target_dir: str=None, file_type: str=None) -> list[str]:
    if target_dir == None:
        target_dir = sys.argv[1]

    if file_type == None:
        file_type = sys.argv[2]

    img_files = os.listdir(target_dir)

###########################################################################
#                            Get all jpeg files                           #
###########################################################################

    img_files = get_files(img_files, file_type)

    ###############################################################################
    #                    Get the sequence numeral from filename                   #
    ###############################################################################

    img_files_ranked = [each_split[0:-1] + each_split[-1].split(".") for each_split in [img_file.split("_") for img_file in img_files]]

    img_files_ranked.sort(key=lambda x: x[-2])

    ###############################################################################
    #                  Get original filename from sorted sequence                 #
    ###############################################################################


    img_files_ranked = [ each_file[0:-1] for each_file in img_files_ranked]

    img_files_ranked = ['_'.join(file_name) for file_name in img_files_ranked]

    img_files_ranked = [ each_file+"."+file_type for each_file in img_files_ranked]

    return img_files_ranked


def rename_img_files():
    # Todo rename files based on sequence numbber
    pass

def get_files(list_of_filenames: str, file_type: str) -> list[str]:
    print("Getting files of type", file_type)
    length = len(file_type)
    img_files = [img_name  for img_name in list_of_filenames if img_name[len(img_name)-length:len(img_name)] == file_type]

    return img_files


if __name__ == "__main__":
    res = file_order_sorter()
    print(res)
