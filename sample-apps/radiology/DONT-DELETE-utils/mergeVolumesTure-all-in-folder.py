# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import glob
import os
import shutil

import monai
from monai.data import DataLoader, list_data_collate
from monai.transforms import Compose, LoadImaged, SaveImaged

data_dir = "/home/andres/Documents/workspace/disk-workspace/Datasets/radiology/brain/NeuroAtlas-Labels/DrTures/all-images/co-registered-volumes/DrTure/ALL-CASES/"
output_folder = "/home/andres/Documents/workspace/disk-workspace/Datasets/radiology/brain/NeuroAtlas-Labels/DrTures/all-images/co-registered-volumes/DrTure/merged/"


set_transforms = Compose(
    [
        LoadImaged(keys="image"),
        SaveImaged(keys="image", output_postfix="", output_dir=output_folder, separate_folder=False),
    ]
)

images = glob.glob(os.path.join(data_dir, "*/*"))
loader_d = []
all_patients = []

# Getting all unique patients
for p in images:
    _, file = os.path.split(p)
    p_name = file.split("-")[1]
    if p_name not in all_patients:
        all_patients.append(p_name)

# creating dict for merging files
for patient in all_patients:
    path_imgs = []
    for mod in ["FLAIR", "T1", "T1C", "T2"]:
        path_img = data_dir + "/Ture-" + patient + "/Ture-" + patient + "-" + mod + ".nrrd"
        path_imgs.append(path_img)
    loader_d.append({"image": path_imgs})


print(len(loader_d))

train_ds = monai.data.Dataset(data=loader_d, transform=set_transforms)
trainLoader = DataLoader(train_ds, batch_size=1, num_workers=1, collate_fn=list_data_collate)


for idx, img in enumerate(trainLoader):
    dirname, file = os.path.split(img["image_meta_dict"]["filename_or_obj"][0])
    tures_number = file.split("-")[1]
    print("Processing image: ", tures_number + ".nii.gz")
    # time.sleep(2)
    filename, extension = os.path.splitext(file)
    shutil.move(output_folder + filename + ".nii.gz", output_folder + "Ture-" + tures_number + ".nii.gz")