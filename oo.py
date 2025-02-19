# import os

# def copy_filenames(src_folder, dest_folder):
#     # 获取源文件夹中的所有文件名
#     filenames = os.listdir(src_folder)
    
#     # 遍历目标文件夹中的所有文件
#     for i, file in enumerate(os.listdir(dest_folder)):
#         src_file = os.path.join(src_folder, filenames[i])
#         dest_file = os.path.join(dest_folder, file)
#         os.rename(dest_file, os.path.join(dest_folder, filenames[i]))

# # 示例用法
# src_folder = 'D:\\Model_evaluation_accelerated_Flask\\static\\images\\213123\\brain\\original'
# dest_folder = 'D:\\Model_evaluation_accelerated_Flask\\static\\images\\213123\\brain\\AI_DICOM'
# copy_filenames(src_folder, dest_folder)
# import numpy as np
# import pydicom
# from pydicom.dataset import Dataset, FileMetaDataset
# from pydicom.filebase import DicomBytesIO
# import h5py

# # 打开 HDF5 文件
# with h5py.File('D:\\Model_evaluation_accelerated_Flask\\static\\images\\image\\test\\kdata_slice32.mat', 'r') as f:
#     # 列出文件中的所有数据集
#     print(list(f.keys()))
    
#     # 假设图像数据存储在名为 'image' 的数据集中
#     matrix = np.array(f['kdata'])

# # 创建一个512x403x32的复数双精度矩阵
# matrix = np.random.rand(512, 403, 32) + 1j * np.random.rand(512, 403, 32)

# # 创建一个空的DICOM数据集
# ds = Dataset()

# # 必须先添加一个File Meta Information header
# ds.file_meta = FileMetaDataset()
# ds.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'  # 例如，CT Image Storage
# ds.file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
# ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

# # 添加一些必要的DICOM标签
# ds.PatientName = "TestFirstname"
# ds.PatientID = "123456"
# ds.is_little_endian = True
# ds.is_implicit_VR = True

# # 由于DICOM通常不支持复数数据，我们需要将复数矩阵转换为实数矩阵。
# # 一种常见的方法是将实部和虚部分开存储，或者计算模和相位。
# # 在这里，我们将实部和虚部作为两个序列存储。

# # 创建实部和虚部的DICOM序列
# real_seq = pydicom.dataset.Sequence()
# imag_seq = pydicom.dataset.Sequence()

# # 为每个切片添加实部和虚部
# for slice_idx in range(matrix.shape):
#     real_item = pydicom.dataset.Dataset()
#     real_item.ImageData = matrix[:, :, slice_idx].real.tobytes()
#     real_seq.append(real_item)
    
#     imag_item = pydicom.dataset.Dataset()
#     imag_item.ImageData = matrix[:, :, slice_idx].imag.tobytes()
#     imag_seq.append(imag_item)

# # 将序列添加到DICOM数据集中
# ds.RealPartSequence = real_seq
# ds.ImaginaryPartSequence = imag_seq

# # 保存DICOM文件
# filename = "complex_matrix.dcm"
# with open(filename, "wb") as f:
#     f.write(ds.as_buffer())

# print(f"DICOM file {filename} has been created.")
# import os
# from plistlib import UID
# from PIL import Image

import cv2
import pydicom as pd
def png_to_dicom(input_filepath, output_dcm_path):
    png_image = cv2.imread(input_filepath, cv2.IMREAD_GRAYSCALE)  # 以灰度模式读取
    template_dicom = pd.dcmread("D:\\Model_evaluation_accelerated_Flask\\TEST.dcm")
    ds = template_dicom.copy()
    ds.file_meta.FileMetaInformationGroupLength = 184
    ds.file_meta.FileMetaInformationVersion = b'\x00\x01'
    ds.file_meta.MediaStorageSOPClassUID = pd.uid.UID('1.2.840.10008.5.1.4.1.1.7')
    ds.file_meta.MediaStorageSOPInstanceUID =pd.uid.generate_uid()
    ds.file_meta.TransferSyntaxUID = pd.uid.UID('1.2.840.10008.1.2')
    ds.file_meta.ImplementationClassUID = pd.uid.UID('1.2.276.0.7230010.3.0.3.5.4')
    ds.file_meta.ImplementationVersionName = 'ANNET_DCMBK_100'



    ds.Rows = png_image.shape[0]
    ds.Columns = png_image.shape[1]
    ds.SamplesPerPixel = 1  # 灰度图像通常是1
    ds.PhotometricInterpretation = "MONOCHROME2"  # 灰度图像通常是MONOCHROME2
    ds.PixelRepresentation = 0  # 无符号整数
    ds.BitsStored = 16  # 每个像素存储的位数（与你的NumPy数组dtype匹配）
    ds.BitsAllocated = 16  # 每个像素分配的位数（通常与BitsStored相同）
    ds.HighBit = 15  # 最高有效位（对于16位图像是15）
    ds.PatientID = "123456"
    ds.PatientBirthDate = "19700101"
    ds.PatientSex = "M"
    ds.PatientName = "Anonymous"
    ds.StudyDescription = "PNG to DICOM"
    ds.SamplesPerPixel = 1
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    # 数据显示格式
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = png_image.tobytes()  # 直接使用灰度图像的字节数据

    # 保存DICOM数据集到文件
    ds.is_little_endian = True
    ds.is_implicit_VR = True  # 使用隐式VR
    ds.PixelData = png_image.tobytes()

    # 保存新的DICOM文件
    ds.save_as(output_dcm_path)
png_to_dicom('1.png', '1.dcm')


# import os
# import subprocess
# # subprocess.run(['static\\images\\Step3_Demo_pFISTA_Radial_Reconstruction.exe','static\\images\\213123\\weqe\\originalmat\\raw_002.data','static\\images\\213123\\weqe','7','Pseudo golden angle'], check=True) 
# subprocess.run(['static\\images\\Step3_Demo_pFISTA_Radial_Reconstruction_ga.exe','testdata\\ga_raw\\originalmat\\UID_159671394896148_gre_radial__sos_3d.raw','testdata\\ga_raw','6','Golden angle',"no"], check=True)        