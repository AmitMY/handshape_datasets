from prettytable import PrettyTable

from .utils import extract_zip, download_file
from handshape_datasets.dataset_loader import DatasetLoader
from skimage import io
import csv
import os
import numpy as np
from enum import Enum
from os import listdir
from .common import *

labels=["Puño","Mano Plana B","Duo Inclinado", "Duo","Pulgar","Cuernos", "L", "Meñique","Miton", "Tres Alternativo"]

class CiarpVersion(Enum):
    WithoutGabor = "WithoutGabor"
    WithGabor = "WithGabor"

class CiarpInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n CIARP
        \n Convolutional neural network-based algorithm for recognition of hand postures on images acquired by a single
        \n color camera
        \n More details can be found at https://link.springer.com/chapter/10.1007/978-3-319-75193-1_53
        \n"""
        url_info = "https://link.springer.com/chapter/10.1007/978-3-319-75193-1_53"
        download_size = 11067633
        disk_size = 19496078
        subject = 7127
        super().__init__("Ciarp",(38,38,1),{"y":"classes", "subject":"subject"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return Ciarp()

class Ciarp(DatasetLoader):
    def __init__(self,version=CiarpVersion.WithoutGabor):
        super().__init__("ciarp")
        self.url = 'http://home.agh.edu.pl/~bkw/code/ciarp2017/ciarp.zip'
        self.filename = self.name + '.zip'
        self.version=version

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        filepath = os.path.join(folderpath, self.filename)
        download_file(url=self.urls(), filepath=filepath)
        # set the exit flag
        self.set_downloaded(folderpath)

    def read_csv(self,txt_path):
        with open(txt_path) as f:
            print(txt_path)
            reader = csv.reader(f,delimiter=' ')
            filename,y=zip(*reader)
            y=np.array(list(map(int,y )))
        return filename,y

    def load_folder(self,folder,txt_path):

        filenames,y=self.read_csv(txt_path)
        x=np.zeros( (len(y),38,38,1),dtype="uint8")
        for i,filename in enumerate(filenames):
            filepath=os.path.join(folder.path,filename)
            image=io.imread(filepath)
            image=image[:,:,np.newaxis]
            x[i,:]=image
        return x,y

    def load(self,folderpath, **kwargs):
        dataset_folder = os.path.join(folderpath , 'ciarp')

        self.folder_image=folderpath
        if 'version' in kwargs:
            if (kwargs['version']!='WithGabor'):
                version_string=self.version.value
            else:
                version_string='WithGabor'
        else:
            version_string=self.version.value
        folders = [f for f in os.scandir(dataset_folder) if f.is_dir() and f.path.endswith(version_string)]

        result={}
        cant_images=0
        for (i, folder) in enumerate(folders):  #Counts the amount of images
           images = list(
               filter(lambda x: ".db" not in x,
                      listdir(str(dataset_folder) + f"\{folder.name}"))
           )
           cant_images = len(images) + cant_images
        j=0
        h = 0
        i=0
        subject = np.zeros(cant_images)
        xtot=np.zeros((cant_images, 38, 38, 1), dtype="uint8")
        ytot=np.zeros(cant_images)
    #Loop x to copy data into xtot
        for folder in folders:

            txt_name=f"{folder.name}.txt"
            txt_path=os.path.join(dataset_folder,txt_name)
            x,y=self.load_folder(folder,txt_path)
            for valuesy in y:
                ytot[j] =valuesy
                j += 1
            for valuesx in x:
                xtot[h]=valuesx
                subject[h]=i
                h += 1
            i+=1
            result[folder.name]=(x,y)
        metadata={"y":ytot, "Type":subject}
        #i show folder code
        table= PrettyTable (["Valor", "Código de carpeta"])
        table.add_row([0, "test_DifferentCamera"])
        table.add_row([1, "test_Kinect"])
        table.add_row([2, "train_Kinect"])
        print(table)
        return xtot,metadata #result contains 3 arrays and returns the 3 prepocess. Each result cointains their x(images) and their y(class)



    def preprocess(self, folderpath):

        zip_path = os.path.join(folderpath, self.filename)
        # extract the zip into the images path
        extract_zip(zip_path, folderpath)
        #remove the zip file
        os.remove(zip_path)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder=os.path.join(fpath,'ciarp')
        npz_exist = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(npz_exist)==0):
            return print("npz not found")
        else:
           rmtree(folder)
           print("Folders delete")
        return True
    #