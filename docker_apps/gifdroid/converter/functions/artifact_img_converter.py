import os
import sys

def find_image_sequence():
    target_dir = sys.argv[1]

    img_files = os.listdir(target_dir)

    ###########################################################################
    #                            Get all jpeg files                           #
    ###########################################################################

    img_files = get_jpeg_files(img_files)

    ###############################################################################
    #                    Get the sequence numeral from filename                   #
    ###############################################################################

    img_files_ranked = [each_split[0:-1] + each_split[-1].split(".") for each_split in [img_file.split("_") for img_file in img_files]]

    img_files_ranked.sort(key=lambda x: x[-2])

    ###############################################################################
    #                  Get original filename from sorted sequence                 #
    ###############################################################################

    img_files_ranked = [''.join(file_name) for file_name in img_files_ranked]

    return img_files_ranked


def rename_img_files():
    # Todo rename files based on sequence numbber
    pass

def get_jpeg_files(list_of_filenames: str) -> list[str]:
    img_files = [img_name  for img_name in list_of_filenames if img_name[len(img_name)-3:len(img_name)] == "jpg"]

    return img_files


if __name__ == "__main__":
    find_image_sequence()
