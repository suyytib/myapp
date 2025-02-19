import cv2
import numpy as np
from skimage import io
import os
from flask import Blueprint
from flask import render_template

from matplotlib import pyplot as plt
import pydicom as pd
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.metrics import structural_similarity as compare_ssim
def rel_norm_error(x, y):
    norm_diff = np.linalg.norm(x - y)
    norm_x = np.linalg.norm(x)
    return norm_diff / norm_x
pathb = "D:\\Model_evaluation_accelerated_Flask\\static\\images\\213123\\brain\\AI_WpFISTA_DICOM"
patha = "D:\\Model_evaluation_accelerated_Flask\\static\\images\\213123\\brain\\AI_DICOM"
pathc = "D:\\Model_evaluation_accelerated_Flask\\static\\images\\213123\\brain\\GT_DICOM"
pathd = "D:\\Model_evaluation_accelerated_Flask\\static\\images\\213123\\brain\\pFISTA_DICOM"
def get_filenames(file_dir,file_type):
    filenames=[]
    if not os.path.exists(file_dir):
        return -1
    for root,dirs,names in os.walk(file_dir):
        for filename in names:
            if os.path.splitext(filename)[1] == file_type:
                filenames.append(os.path.join(root,filename))
    return filenames
a=get_filenames(patha,".dcm")
b=get_filenames(pathb,".dcm")
PSNRa=0
SSIMa=0
RLNEa=0
for t in range(len(a)):
    imga= pd.dcmread(a[t])
    imga =imga.pixel_array
    imga = imga.astype(np.float32) / np.max(imga) 
    imgb= pd.dcmread(b[t])
    imgb =imgb.pixel_array
    imgb = imgb.astype(np.float32) / np.max(imgb) 
    PSNRa+=compare_psnr(imga, imgb)
    ab=imga.max()-imgb.min()
    SSIMa+=compare_ssim(imga, imgb,data_range=ab, multichannel=True)
    RLNEa+=rel_norm_error(imga, imgb)

a=get_filenames(patha,".dcm")
b=get_filenames(pathc,".dcm")
PSNRb=0
SSIMb=0
RLNEb=0
for t in range(len(a)):
    imga= pd.dcmread(a[t])
    imga =imga.pixel_array
    imga = imga.astype(np.float32) / np.max(imga) 
    imgb= pd.dcmread(b[t])
    imgb =imgb.pixel_array
    imgb = imgb.astype(np.float32) / np.max(imgb) 
    PSNRb+=compare_psnr(imga, imgb)
    ab=imga.max()-imgb.min()
    SSIMb+=compare_ssim(imga, imgb,data_range=ab, multichannel=True)
    RLNEb+=rel_norm_error(imga, imgb)

a=get_filenames(patha,".dcm")
b=get_filenames(pathd,".dcm")
PSNRc=0
SSIMc=0
RLNEc=0
for t in range(len(a)):
    imga= pd.dcmread(a[t])
    imga =imga.pixel_array
    imga = imga.astype(np.float32) / np.max(imga) 
    imgb= pd.dcmread(b[t])
    imgb =imgb.pixel_array
    imgb = imgb.astype(np.float32) / np.max(imgb) 
    PSNRc+=compare_psnr(imga, imgb)
    ab=imga.max()-imgb.min()
    SSIMc+=compare_ssim(imga, imgb,data_range=ab, multichannel=True)
    RLNEc+=rel_norm_error(imga, imgb)


print("PSNRa: {0}".format(PSNRa/len(a)))
print("SSIMa: {0}".format(SSIMa/len(a)))
print("RLNEa: {0}".format(RLNEa/len(a)))
print("PSNRb: {0}".format(PSNRb/len(a)))
print("SSIMb: {0}".format(SSIMb/len(a)))
print("RLNEb: {0}".format(RLNEb/len(a)))
print("PSNRc: {0}".format(PSNRc/len(a)))
print("SSIMc: {0}".format(SSIMc/len(a)))
print("RLNEc: {0}".format(RLNEc/len(a)))