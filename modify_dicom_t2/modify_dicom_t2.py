# -*- coding: utf-8 -*-
"""
23 Apr 2021
Script to correct baseline T2-prep scans (so data can be analysed in cvi42 or Segment)
"""
import pydicom
import os.path
import shutil
import easygui
import re

#function to read T2 prep times from dicom header
def get_prep_times_VE11(dicom_hdr):
    
    #define regular expressions
    prep_times_re = r'sPrepPulses.adT2PrepDuration.__attribute__.size[ ]+=[ ]+([\d]+)'
    prep_times_value_re = r'sPrepPulses.adT2PrepDuration\[\d+\][ ]+=[ ]+([.\d]+)'
 
    out = repr(dicom_hdr[(0x0029, 0x1020)].value) #This field contains all of MeasYaps
    out = out.replace('\\t', ' ')
    out = out.replace('\\n', '\n')
    
    prep_time_search = re.findall(prep_times_re, out)
    if not prep_time_search:
        return []
    else:
        num_preps = int(prep_time_search[0])
        prep_times = re.findall(prep_times_value_re, out)[0:num_preps]
        return prep_times

   


def fix_baseline(in_folder, out_folder):
    
    fname_list=os.listdir(in_folder)
    dicom_list=[fname for fname in fname_list if '.ima' in fname or '.IMA' in fname or '.dcm' in fname] #find all dicoms
    for index, dicom_filename in enumerate(dicom_list): #go through all dicoms, if prep time = 0 (baseline), 
                                                        #change to prep time = 2000
        ds = pydicom.dcmread(os.path.join(in_folder, dicom_filename))
        
        if hasattr(ds, 'ImageComments'): #ImageComments field is only pre-written in VE11C
            # comment_str = ds.ImageComments
            # comment_str_new = comment_str.replace(' 0', ' 2000')
            comment_str_new = ds.ImageComments
            if not comment_str_new.startswith('T2'):
                tmp = comment_str_new.split(', ')
                comment_str_new = tmp[1]

            ds.ImageComments = comment_str_new
        
        else:  # VE11B - need to add ImageComments field with prep times
            if index==0: #get list of all prep times - each dicom file has the list of all prep times 
                         #in the sequence, so only need to do this once
                prep_time_list = get_prep_times_VE11(ds)
                print(prep_time_list)

                
                if len(prep_time_list) == len(dicom_list) - 1: #On VE11B Tprep=0 doesn't show up in prep time list.
                                                           #Assuming here that Tprep=0 is the first scan.
                    prep_time_list.insert(0,'2000')

                elif len(prep_time_list) < len(dicom_list) -1 or len(prep_time_list) > len(dicom_list):

                    raise ValueError('Number of preps in acquisition does not match number of images. Maybe this is not a T2-prepared scan...')

            InstanceNumber = int(ds.InstanceNumber)   
            ds.ImageComments = 'T2 prep. duration = ' + prep_time_list[InstanceNumber - 1].split('.')[0] + ' ms'


        ds.save_as(os.path.join(out_folder, dicom_filename))

    return True

def main():
    in_folder = easygui.diropenbox()
    out_folder = os.path.join(os.path.dirname(in_folder), (os.path.basename(in_folder) + '_corrected'))

    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.mkdir(out_folder)
    try:
        fix_baseline(in_folder, out_folder)
    except Exception as e:
        easygui.msgbox(str(e))
        os.rmdir(out_folder)
        return

    easygui.msgbox('Created folder \'' + out_folder +'\'', 'ModifyDicomT2')


if __name__ == '__main__':
    main()
    
    