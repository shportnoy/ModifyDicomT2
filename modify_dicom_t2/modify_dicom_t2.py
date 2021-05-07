# -*- coding: utf-8 -*-
"""
23 Apr 2021
Script to correct baseline T2-prep scans (so data can be analysed in cvi42 or Segment)
"""
import pydicom
import os.path
import shutil
import easygui

def fix_baseline(in_folder, out_folder):
    
    fname_list=os.listdir(in_folder)
    dicom_list=[fname for fname in fname_list if '.IMA' in fname or '.dcm' in fname] #find all dicoms
    for index, dicom_filename in enumerate(dicom_list): #go through all dicoms, if prep time = 0 (baseline), 
                                                        #change to prep time = 2000
        ds = pydicom.dcmread(os.path.join(in_folder, dicom_filename))
        comment_str = ds.ImageComments
        ds.ImageComments = comment_str.replace('0','2000')
        ds.save_as(os.path.join(out_folder,dicom_filename))


def main():
    in_folder = easygui.diropenbox()
    out_folder = os.path.join(os.path.dirname(in_folder), (os.path.basename(in_folder) + '_fixed'))

    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.mkdir(out_folder)

    fix_baseline(in_folder, out_folder)


if __name__ == '__main__':
    main()
    
    