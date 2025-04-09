# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:53:07 2024

@author: aawad
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
import os
import random
from image_inference import infer_image
from PIL import Image, ImageDraw, ImageFont
import cv2
from super_gradients import setup_device
#########################################################################################################
models = ["Original", "ACDC","TEBCF", "BayesRet", "PCDE", "ICSP", "AutoEnh", "Semi-UIR", "USUIR", "TUDA"]
mAP_CSV_dir = r"C:\Users\aawad\Desktop\Models Implemented\yolo-nas\super-gradients\results".replace('\\', '/')
project_dir =  r"C:\Users\aawad\Desktop\Detecction Enhancement Corrolation".replace('\\', '/')
Qindex_CSV_dir = r"C:\Users\aawad\Desktop\IEEE Trans Sets\Q-index".replace('\\', '/')
save_dir = project_dir
dataset = 'RUOD' #RUOD OR CUPDD
extracted_field_mAP = 'mAP'
extracted_field_Qindex = 'Q-index'
index_field = 'images'
label_size = (800, 200)
max_image_size = (800, 600)
image_root_dir = r"C:\Users\aawad\Desktop\Models Implemented\yolo-nas\super-gradients\data\Enhanced_RUOD_yolo".replace('\\','/')
extension = r'*.jpg'
#label_folder = r"labels"
images_per_folder = 5

setup_device(device= 'cuda')
DEVICE = 'cuda'
#extf = set((f'{root_dir}\Orignial\$RECYCLE.BIN\\', f'{root_dir}\Orignial\System Volume Information\\'))
#groups = glob.glob(f'{root_dir}\Original\\*', recursive=True)
#groups = [os.path.basename(os.path.split(d)[0]) for d in groups if d not in extf]

def generate_labels(labels, label_size = (800, 200), fontSize = 75, text_offset = 0, rotation = 0, line = False):
    images = []
    for label in labels:
        print(label)
        width, height = label_size
    
        font = ImageFont.truetype("arial.ttf", size=fontSize)
        img = Image.new('RGB', (width, height), color='white')
        
        imgDraw = ImageDraw.Draw(img)
        
        _, _, textWidth, textHeight = imgDraw.textbbox((0, 0),label, font=font)
        xText = (width - textWidth) / 2
        yText = ((height - textHeight) / 2) + text_offset #to shift the text up and down
        
        if line:
            imgDraw.line((0,0, width,0), fill=(100, 100, 100), width=20) #please comment this when generating titles (lowQ, etc)
        imgDraw.text((xText, yText), label, font=font, fill=(0, 0, 0))
        
        # Save image
        img.convert("RGBA")
        img = img.rotate(rotation, expand=True)
        images.append(img)
    return images

def combine_images(columns, space, images, ispath = False):
    rows = len(images) // columns
    if len(images) % columns:
        rows += 1
    width_sum = sum(image.size[0] for image in images)
    height_sum = sum(image.size[1] for image in images)    

    background_width = width_sum//rows + (space*columns)-space
    background_height = height_sum//columns  + (space*rows)-space
    background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))
    x = 0
    y = 0
    for i, img in enumerate(images):
        if ispath:
            img = Image.open(img)

        background.paste(img, (x, y))
        x += img.width + space
        if (i+1) % columns == 0:
            y += img.height + space
            x = 0
    return background

df_metric = pd.DataFrame()
df_Q_all = pd.DataFrame()

for  model in models:
    df_model = pd.read_csv(f'{mAP_CSV_dir}/{dataset}/{model}_mAP.csv', dtype=str)
    df_metric[f'{model}'] = df_model[f'{extracted_field_mAP}'.split(' ')[0]]
    df_Q = pd.read_csv(f'{Qindex_CSV_dir}/{dataset}/{model}.csv', index_col=0)
    df_Q_all[f'{model}'] = df_Q[f'{extracted_field_Qindex}'.split(' ')[0]].round(2)


##################################################################################################################
#post processing to add the index field with the propoer prefix and convert other columns to the right data type
#because I saved those CSV wrong
df_metric[index_field] = df_model[index_field]
df_metric[index_field] = df_metric[index_field] + '.jpg'
df_metric.set_index(index_field, inplace=True)
df_metric = df_metric.astype(float)
###################################################################################################################

df_Q_all = df_Q_all[df_Q_all.index.isin(df_metric.index)] #get the Q-index indecies that match the indecies in the mAP dataframe

df_max = pd.DataFrame(index=df_metric.index)
df_max['Max mAP'] = df_metric.max(axis=1)
df_max['Model'] = df_metric.idxmax(axis=1)

Q_values = []
for i in range(len(df_Q_all)):
    Q_values.append(df_Q_all[df_max["Model"].iloc[i]].iloc[i])
df_max["Q-index"] = Q_values

selected = df_max.drop_duplicates("Model").sample(n=10) #pick random samples
selected = selected.reindex(selected['Model'].map(dict(zip(models, range(len(models))))).sort_values().index) #reorder based on models var
selected = selected[selected["Model"] !="Original"] # delete 'original' entry
#selected_path = random.sample(glob.glob(f"{image_root_dir}\Original\{extension}"), images_per_folder)
#selected = [os.path.basename(image) for image in selected_path]
org_images_path = []
enh_images_path = []
org_mAP_selected = []
enh_mAP_selected = []
org_Q_selected = []
enh_Q_selected = []
for index, row in selected.iterrows():
    org_images_path.append(glob.glob(f'{image_root_dir}/Original/test/images/**/{index}', recursive=True)[0].replace('\\', '/'))
    enh_images_path.append(glob.glob(f'{image_root_dir}/{row.Model}/test/images/**/{index}', recursive=True)[0].replace('\\', '/'))
    org_mAP_selected.append(df_metric["Original"][index])
    enh_mAP_selected.append(df_metric[row.Model][index])
    org_Q_selected.append(df_Q_all["Original"][index])
    enh_Q_selected.append(df_Q_all[row.Model][index])
    
original_selected = {"images": org_images_path, "mAP": org_mAP_selected, "Q-index": org_Q_selected}
enhanced_selected = {"images": enh_images_path, "mAP": enh_mAP_selected, "Q-index": enh_Q_selected}

labels = ["mAP= " + str(x[0]) + "\n" + "Q-index= " + str(x[1]) for x in zip(org_mAP_selected, org_Q_selected)]
org_label_metrics = generate_labels(labels, label_size)
#labels = ["mAP= " + str(x[1]) + "\n" + "Q-index= " + str(x[2]) + "\n" + x[0] for x in zip(selected["Model"], enh_mAP_selected, enh_Q_selected)]
labels = ["mAP= " + str(x[0]) + "\n" + "Q-index= " + str(x[1]) for x in zip(enh_mAP_selected, enh_Q_selected)]
enh_label_metrics = generate_labels(labels, label_size)
label_cols =  generate_labels(selected["Model"], label_size, line = True)
labels = ["GT", "Original", "Enhanced"]
label_rows = generate_labels(labels, label_size, rotation = 90)

gt_images_selected = []
org_images_selected = []
for i, image in enumerate(org_images_path):
    gt_images_selected.append(infer_image(image,  gt = True))
    org_images_selected.append(infer_image(image))
    #gt_images_selected.append(Image.open(rf"C:\Users\aawad\Desktop\x\gt\{i}.jpg"))
    #org_images_selected.append(Image.open(rf"C:\Users\aawad\Desktop\x\org\{i}.jpg")) 
enh_images_selected = []
for i, image in enumerate(enh_images_path):
    enh_images_selected.append(infer_image(image))
    #enh_images_selected.append(Image.open(rf"C:\Users\aawad\Desktop\x\enh\{i}.jpg"))

layers_mat = []

layers_mat.append(combine_images(columns=len(models)-1, space=20, images = gt_images_selected))
layers_mat.append(combine_images(columns=len(models)-1, space=20, images = org_images_selected))
layers_mat.append(combine_images(columns=len(models)-1, space=20, images = org_label_metrics))
#
layers_mat.append(combine_images(columns=len(models)-1, space=20, images = enh_images_selected))
layers_mat.append(combine_images(columns=len(models)-1, space=20, images = enh_label_metrics))
layers_mat.append(combine_images(columns=len(models)-1, space=20, images = label_cols))

all_layers = combine_images(columns=1, space=20, images = layers_mat)
layer_row = combine_images(columns=1, space=20, images = label_rows)

final = combine_images(columns=2, space=20, images = [layer_row, all_layers])


#figure=np.concatenate((all_layers, layers_mat[5]),axis=0)
figure = np.asarray(final)
# Save without a cmap, to preserve the ones you saved earlier
plt.imsave(f'{save_dir}/{dataset}.jpeg',figure,cmap=None, format='jpeg')














