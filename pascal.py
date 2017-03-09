"""
This code is going to build a dataset with the selected amouts of training samples and validation ones
"""
import os
import argparse
import xml.etree.ElementTree as ET
import shutil


# Recieve path of actions40 directory
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--data_path",
                    help="Number of train samples in the DB",
                    default="../PascalVOC2012")
args = parser.parse_args()
data_path = args.data_path
if data_path[-1] != '/' : data_path += '/'



def build_dataset(official_splits = True):
    """
    From the directory we are at, this function creates a data directory with desired splits (train & valid)

    # Parameters
        official_splits : whether or not we consider the official valid set
                          not anotated set
    """
    from shutil import copyfile, rmtree
    if os.path.isdir(data_path+'data'):
        rmtree(data_path+'data')
    os.mkdir(data_path+"data")
    os.mkdir(data_path+"data/train")
    os.mkdir(data_path+"data/valid")
    os.mkdir(data_path+"data/test")

    # Get set files with image names
    img_name_files = {}
    img_name_files['train'] = [f for f in os.listdir(data_path+"/ImageSets/Main/")
                               if '_train' in f]
    img_name_files['valid'] = [f for f in os.listdir(data_path+"/ImageSets/Main/")
                               if '_val' in f]
    img_name_files['test'] = [f for f in os.listdir(data_path+"/ImageSets/Main/")
                               if 'test.txt' == f]

    for set_name, files_in_set in img_name_files.items():
        for file_name in files_in_set:
            # Get class name & create corresponding folder
            class_name = file_name.split('_')[0]
            class_folder_path = data_path+"data/"+set_name+"/"+class_name+'/'
            if not os.path.isdir(class_folder_path):
                os.makedirs(class_folder_path)

            # copy files
            print data_path+"ImageSets/Main/"+file_name
            with open(data_path+"ImageSets/Main/"+file_name, 'r') as mfile:
                for line in mfile:
                    if line[-3] is not "-":
                        # copy this file
                        to_cp = line.split(" ")[0]
                        copyfile(data_path+"JPEGImages/"+to_cp+".jpg",
                                 class_folder_path+to_cp+".jpg")


build_dataset(official_splits = True)
