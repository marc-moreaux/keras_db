"""
This code is going to build a dataset with the selected amouts of training samples and validation ones
"""
import os
import argparse
import xml.etree.ElementTree as ET


# Recieve path of actions40 directory
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--data_path",
                    help="Number of train samples in the DB",
                    default="../actions40")
parser.add_argument("--official",
                    help="use the official splits (no test set) (true or false)",
                    default="true")

args = parser.parse_args()
data_path = args.data_path
official_splits = True if args.official == "true" else False
if data_path[-1] != '/' : data_path += '/'


def build_dataset(official_splits = True):
    """
    From the directory we are at, this function creates a data directory with desired splits (train & valid)

    # Parameters
        official_splits : whether or not we consider the official valid set
                          not anotated set
    """
    from shutil import copyfile, rmtree

    dir_name = 'data' if official_splits == True else 'data2'

    if os.path.isdir(data_path+dir_name):
        rmtree(data_path+dir_name)
    os.mkdir(data_path+dir_name)
    os.mkdir(data_path+dir_name+"/train")
    os.mkdir(data_path+dir_name+"/valid")
    if official_splits == False:
        os.mkdir(data_path+dir_name+"/test")


    # Get files with splits
    # Get files with splits
    files = os.listdir(data_path+"ImageSplits/")
    for file_name in files:
        if(file_name != "actions.txt" and
           file_name != "test.txt" and
           file_name != "train.txt"):
            with open(data_path+"ImageSplits/"+file_name, 'r') as mfile:
                for img_idx, img_name in enumerate(mfile.readlines()):
                    # Remove some bullshit on strings
                    img_name = img_name.strip('\n').strip('\t').strip('\r')

                    # eg. applauding_test.txt to test
                    set_name = file_name.split('_')[-1][:-4]
                    if official_splits == True:
                        # Rename test to valid
                        if set_name == "test":
                            set_name = "valid"
                    else:
                        # Create a split between valid and test
                        if (set_name == "test") and (img_idx > 49):
                            set_name = "valid"

                    if img_idx == 1000:
                        print(img_idx, img_name, set_name)

                    # eg. looking_through_mic_047.jpg to looking_through_mic
                    class_name = img_name.split("_")[:-1]
                    class_name = "_".join(class_name)

                    # Add localisation information to img_name
                    xml_name = img_name.split('.')[0]+'.xml'
                    root = ET.parse(data_path+"XMLAnnotations/"+xml_name).getroot()
                    bottom = int(root.find('object').find('bndbox').find('ymax').text)
                    right = int(root.find('object').find('bndbox').find('xmax').text)
                    left = int(root.find('object').find('bndbox').find('xmin').text)
                    top = int(root.find('object').find('bndbox').find('ymin').text)
                    im_w = float(root.find('size').find('width').text)
                    im_h = float(root.find('size').find('height').text)

                    bottom = int(bottom*(224/im_h))
                    right = int(right*(224/im_w))
                    left = int(left*(224/im_w))
                    top = int(top*(224/im_h))

                    pos_string = "_{}_{}_{}_{}".format(top,left,bottom,right)
                    img_name_new = img_name.split('.')[0]+pos_string+'.jpg'

                    # mkdir if missing and copy file
                    if not os.path.isdir(data_path+"data2/"+set_name+'/'+class_name):
                        os.mkdir(data_path+"data2/"+set_name+'/'+class_name+'/')
                    copyfile(data_path+"JPEGImages/"+img_name,
                             data_path+"data2/"+set_name+'/'+class_name+'/'+img_name_new)






build_dataset(official_splits=official_splits)
