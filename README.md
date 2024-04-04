# ModifyDicomT2
Modify header information for Myomaps baseline (T2prep=0 ms, Tsat=0 ms) acquisitions. This is required for data analysis in cvi42 or Segment.

Installation
------------
In order to use this software you need to have python installed on your computer. If you don't already have it, the easiest way to get python is to download Anaconda:
https://www.anaconda.com/products/individual

Install ModifyDicomT2 on your computer with the following command:
```bash
pip install git+https://github.com/shportnoy/ModifyDicomT2
```
Running the script
--------------------
Following installation, the script can be launched with the command:
```bash
modify_dicom_t2
````
How it works
------------
1) The script launches with a dialog box asking you to select a folder. Select the folder with the dicom images obtained from the T2-prepared Myomaps scan. 
2) The script will go through the dicoms in the folder and update the header information (specifically, the Image Comments field) for any baseline scan (with Tprep=0).
3) All the dicoms will be copied into a new folder with the same name as the folder you selected in Step 1, appended by *_corrected*.
4) The script closes.
5) Import the *_corrected* folder into cvi42 for T2 fitting.
