# Automated Registration (AREG)

Automated Registration (AREG) is an extension for **3D Slicer** to perform automatic registration either on IOS or CBCT files.

## AREG Modules

AREG module provide a convenient user interface allowing to orient different type of scans:
- **CBCT** scan
- **IOS** scan

## How does the module works?

### 3 Modes Available
- **Orientation and Registration** (to perform the entirety of the workflow automatically: Automatic Orientation, Registration, and Segmentation)
- **Fully-Automated** (to perform the Automatic Mask Generation, Registration and Segmentation)
- **Semi-Automated** (to perform the Automatic Registration and Segmentation)

| Mode | Input |
| ----------- | ----------- |
| Orientation and Registration | Scans|
| Fully-Automated | Oriented Scans |
| Semi-Automated | Oriented Scans, Masks Segmentation Files |


### Input file:

| Input Type  | Input Extension Type |
| ----------- | ----------- |
| **CBCT** | .nii, .nii.gz, .gipl.gz, .nrrd, .nrrd.gz  |
| **IOS** | .vtk |

**<ins>Test Files Available:**
You can either download them using the link or by using the `Test Files` button.
| Module Selected  | Download Link to Test Files | Information |
| ----------- | ----------- | ----------- |
| **Semi-CBCT** | [Test Files](https://github.com/lucanchling/ASO_CBCT/releases/download/TestFiles/Occlusal_Midsagittal_Test.zip) | Scan and Fiducial List for this [Reference](https://github.com/lucanchling/ASO_CBCT/releases/download/v01_goldmodels/Occlusal_Midsagittal_Plane.zip)|
| **Fully-CBCT** | [Test File](https://github.com/lucanchling/ASO_CBCT/releases/download/TestFiles/Test_File.nii.gz) | Only Scan|
| **Semi-IOS** | [Test Files](https://github.com/HUTIN1/ASO/releases/download/v1.0.2/input_test.zip) | Mesh and Fiducial List [Reference](https://github.com/HUTIN1/ASO/releases/download/v1.0.0/Gold_file.zip) |
| **Fully-IOS** | [Test Files](https://github.com/HUTIN1/ASO/releases/download/v1.0.2/input_test.zip)| Only Mesh [Reference](https://github.com/HUTIN1/ASO/releases/download/v1.0.0/Gold_file.zip) |

### Models Selection

For the **Fully-Automated** Mode, models are required as input, use the `Download Models` Button or follow the following instructions:
  
#### For CBCT ([Details](https://github.com/lucanchling/ASO#aso-cbct)):
A *Pre-Orientation* and *ALI_CBCT* models are needed
  

#### For IOS:

### Outputs Options

### Let's Run it


## Algorithm
The implementation is based on iterative closest point's algorithm to execute a landmark-based registration. Some preprocessing steps are done to make the orientation works better (and are described respectively in **CBCT** and **IOS** part)

### ASO CBCT
**Fully-Automated mode:** 
1. a deep learning model is used to predict head orientation and correct it.
Models are available for download ([Pre ASO CBCT Models](https://github.com/lucanchling/ASO_CBCT/releases/tag/v01_preASOmodels))

1. a Landmark Identification Algorithm ([ALI CBCT](https://github.com/DCBIA-OrthoLab/ALI_CBCT)) is used to determine user-selected landmarks

1. an ICP transform is used to match both of the reference and the input file

For the **Semi-Automated** mode, only step **3** is used to match input landmarks with reference's ones.

### ASO IOS

  **Semi-Automated mode:**
 - an ICP transfrom is used to macth both of the reference and the input file by using the landmark
  
  **Fully-Automated mode:**
  
 **<ins> Description of the tool:**


# Acknowledgements
Nathan Hutin (University of Michigan), Luc Anchling (UoM), Felicia Miranda (UoM), Selene Barone (UoM), Marcela Gurgel (UoM), Najla Al Turkestani (UoM), Juan Carlos Prieto (University of North Carolina), Lucia Cevidanes (UoM)


# License
It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0
