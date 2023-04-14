from AREG_Methode.Methode import Methode
from AREG_Methode.Progress import DisplayAREGCBCT, DisplayAMASSS
import os,sys

fpath = os.path.join(os.path.dirname(__file__), '..','..')
sys.path.append(fpath)
from AREG_CBCT.AREG_CBCT_utils.utils import GetDictPatients

import slicer
import time
import qt
import platform

class Semi_CBCT(Methode):
    def __init__(self, widget):
        super().__init__(widget)
        documentsLocation = qt.QStandardPaths.DocumentsLocation
        documents = qt.QStandardPaths.writableLocation(documentsLocation)
        self.tempAMASSS_folder = os.path.join(documents, slicer.app.applicationName+"_temp_AMASSS")

    def getGPUUsage(self):
        if platform.system() == 'Darwin':
            return 1
        else:
            return 5

    def NumberScan(self, scan_folder_t1: str,scan_folder_t2: str):
        return len(GetDictPatients(scan_folder_t1, scan_folder_t2))
        
    def PatientScanLandmark(self, dic, scan_extension, lm_extension):
        patients = {}

        for extension,files in dic.items():
            for file in files:
                file_name = os.path.basename(file).split(".")[0]
                patient = file_name.split('_scan')[0].split('_Scanreg')[0].split('_lm')[0]

                if patient not in patients.keys():
                    patients[patient] = {"dir": os.path.dirname(file),"lmrk":[]}
                if extension in scan_extension:
                    patients[patient]["scan"] = file
                if extension in lm_extension:
                    patients[patient]["lmrk"].append(file)

        return patients
    
    def getReferenceList(self):
        return {
            "Occlusal and Midsagittal Plane": "https://github.com/lucanchling/ASO_CBCT/releases/download/v01_goldmodels/Occlusal_Midsagittal_Plane.zip",
            "Frankfurt Horizontal and Midsagittal Plane": "https://github.com/lucanchling/ASO_CBCT/releases/download/v01_goldmodels/Frankfurt_Horizontal_Midsagittal_Plane.zip",

        }

    def TestReference(self, ref_folder: str):
        out = None
        scan_extension = [".nrrd", ".nrrd.gz", ".nii", ".nii.gz", ".gipl", ".gipl.gz"]
        lm_extension = [".json"]

        if self.NumberScan(ref_folder) == 0 :
            out = 'The selected folder must contain scans'

        if self.NumberScan(ref_folder) > 1 :
            out = 'The selected folder must contain only 1 case'
        
        return None

    def TestCheckbox(self,dic_checkbox):
        list_landmark = self.CheckboxisChecked(dic_checkbox)['Registration Type']
        
        out = None
        if len(list_landmark) == 0:
             out = 'Please select a Registration Type\n'
        return out

    def TestModel(self, model_folder: str,lineEditName) -> str:

        if lineEditName == 'lineEditModel1':
            if len(super().search(model_folder,'pth')['pth']) == 0:
                return 'Folder must have AMASSS masks models files'
            else:
                return None
        
        # if lineEditName == 'lineEditModelAli':
        #     if len(super().search(model_folder,'pth')['pth']) == 0:
        #         return 'Folder must have ALI models files'
        #     else:
        #         return None

    def TestProcess(self, **kwargs) -> str:
        out=''

        testcheckbox = self.TestCheckbox(kwargs['dic_checkbox'])
        if testcheckbox is not None:
            out+=testcheckbox

        if kwargs['input_t1_folder'] == '':
            out+= 'Please select an input folder for T1 scans\n'

        if kwargs['input_t2_folder'] == '':
            out+= 'Please select an input folder for T2 scans\n'

        if kwargs['folder_output'] == '':
            out+= 'Please select an output folder\n'

        if kwargs['add_in_namefile']== '':
            out += 'Please select an extension for output files\n'

        if kwargs['model_folder_1'] == '':
            out += 'Please select a folder for AMASSS models\n'

        if out == '':
            out = None

        return out

    def getSegOrModelList(self):
        return ("AMASSS", {"Full Face Models":"https://github.com/lucanchling/AMASSS_CBCT/releases/download/v1.0.2/AMASSS_Models.zip","Mask Models":"https://github.com/lucanchling/AMASSS_CBCT/releases/download/v1.0.2/Masks_Models.zip"})

    def getALIModelList(self):
        return ("ALIModels", "https://github.com/lucanchling/ALI_CBCT/releases/download/models_v01/")


    def ProperPrint(self,notfound_list):
        dic = {'scanT1':'T1 scan','scanT2':'T2 scan','segT1':'T1 segmentation','segT2':'T2 segmentation'}
        out = ''
        if 'scanT1' and 'scanT2' in notfound_list:
            out += 'T1 and T2 scans\n'
        elif 'segT1' and 'segT2' in notfound_list:
            out += 'T1 and T2 segmentations\n'
        else:
            for notfound in notfound_list:
                out += dic[notfound]+' '
        return out
    
    def TestScan(self, scan_folder_t1: str, scan_folder_t2: str, liste_keys = ['scanT1','scanT2','segT1','segT2']):
        out = ''
        scan_extension = [".nrrd", ".nrrd.gz", ".nii", ".nii.gz", ".gipl", ".gipl.gz"]
        if self.NumberScan(scan_folder_t1,scan_folder_t2) == 0 :
            return 'Please Select folder with scans'
        
        patients = GetDictPatients(scan_folder_t1,scan_folder_t2)
        for patient,data in patients.items():
            not_found = [key for key in liste_keys if key not in data.keys()]
            if len(not_found) != 0:
                out += f"Patient {patient} does not have {self.ProperPrint(not_found)}\n"

        if out == '':   # If no errors
            out = None
            
        return out

        
    def Sugest(self):
        return ['']


    def CheckboxisChecked(self,diccheckbox : dict, in_str = False):
        listchecked = {key:[] for key in diccheckbox.keys()}
        for key,checkboxs in diccheckbox.items():
            for checkbox in checkboxs:
                if checkbox.isChecked():
                    listchecked[key] += [checkbox.text]

        # if not len(diccheckbox) == 0:
        #     for checkboxs in diccheckbox.values():
        #         for checkbox in checkboxs:
        #             if checkbox.isChecked():
        #                 listchecked.append(checkbox.text)
        # if in_str:
        #     listchecked_str = ''
        #     for i,lm in enumerate(listchecked):
        #         if i<len(listchecked)-1:
        #             listchecked_str+= lm+' '
        #         else:
        #             listchecked_str+=lm
        #     return listchecked_str
    
        return listchecked
    
    def DicLandmark(self):
        return {'Registration Type':["Cranial Base","Mandible","Maxilla"],
                'AMASSS Segmentation':['Cranial Base','Cervical Vertebra','Mandible','Maxilla','Skin','Upper Airway']}

    def TranslateModels(self,listeModels,mask=False):
        dicTranslate = {
            "Models": {
                "Mandible" : "MAND",
                "Maxilla" : "MAX",
                "Cranial Base" : "CB",
                "Cervical Vertebra" : "CV",
                "Root Canal" : "RC",
                "Mandibular Canal" : "MCAN",
                "Upper Airway" : "UAW",
                "Skin" : "SKIN",
            },
            "Masks": {
                "Cranial Base": "CBMASK",
                "Mandible": "MANDMASK",
                "Maxilla": "MAXMASK",
            }
        }
        
        translate = ""
        for i,model in enumerate(listeModels):
            if i<len(listeModels)-1:
                if mask:
                    translate += dicTranslate["Masks"][model]+" "
                else:
                    translate += dicTranslate["Models"][model]+" "
            else:
                if mask:
                    translate += dicTranslate["Masks"][model]
                else:
                    translate += dicTranslate["Models"][model]

        return translate
    
    def existsLandmark(self, input_dir, reference_dir, model_dir):
        return None
    

    def getTestFileList(self):
        return ("Semi-Automated", "https://github.com/lucanchling/Areg_CBCT/releases/download/TestFiles/TEST_Semi_AREG.zip")


    def Process(self, **kwargs):
        list_struct = self.CheckboxisChecked(kwargs['dic_checkbox'])
        full_reg_struct,full_seg_struct = list_struct['Registration Type'],list_struct['AMASSS Segmentation']
        reg_struct,seg_struct = self.TranslateModels(full_reg_struct, False),self.TranslateModels(full_seg_struct, False)

        nb_scan = self.NumberScan(kwargs['input_t1_folder'],kwargs['input_t2_folder'])

        list_process = []
        
        # AREG CBCT PROCESS
        AREGProcess = slicer.modules.areg_cbct
        for i,reg in enumerate(reg_struct.split(' ')):
            parameter_areg_cbct = {
                        't1_folder':kwargs['input_t1_folder'],
                        't2_folder':kwargs['input_t2_folder'],
                        'reg_type':reg,
                        'output_folder':kwargs['folder_output'],
                        'add_name':kwargs['add_in_namefile'],
                    }
            list_process.append({'Process':AREGProcess,'Parameter':parameter_areg_cbct,'Module':'AREG_CBCT for {}'.format(full_reg_struct[i]),'Display':DisplayAREGCBCT(nb_scan)})
        
        # AMASSS PROCESS - SEGMENTATION
        list_process = []
        AMASSSProcess = slicer.modules.amasss_cli
        parameter_amasss_seg_t1 = {"inputVolume": kwargs['input_t1_folder'],
                                "modelDirectory": kwargs['model_folder_1'],
                                "highDefinition": False,
                                "skullStructure": seg_struct,
                                "merge": "MERGE" if kwargs['merge_seg'] else "SEPARATE",
                                "genVtk": True,
                                "save_in_folder": False,
                                "output_folder": kwargs['folder_output'],
                                "precision": 50,
                                "vtk_smooth": 5,
                                "prediction_ID": 'Pred',
                                "gpu_usage": self.getGPUUsage(),
                                "cpu_usage": 1,
                                "temp_fold" : self.tempAMASSS_folder,
                                "SegmentInput" : False,
                                "DCMInput": False,
        }              
        parameter_amasss_seg_t2 = {"inputVolume": kwargs['folder_output'],
                                "modelDirectory": kwargs['model_folder_1'],
                                "highDefinition": False,
                                "skullStructure": seg_struct,
                                "merge": "MERGE" if kwargs['merge_seg'] else "SEPARATE",
                                "genVtk": True,
                                "save_in_folder": False,
                                "output_folder": kwargs['folder_output'],
                                "precision": 50,
                                "vtk_smooth": 5,
                                "prediction_ID": 'Pred',
                                "gpu_usage": self.getGPUUsage(),
                                "cpu_usage": 1,
                                "temp_fold" : self.tempAMASSS_folder,
                                "SegmentInput" : False,
                                "DCMInput": False,
        }
        if len(full_seg_struct) > 0:
            list_process.append({'Process':AMASSSProcess,'Parameter':parameter_amasss_seg_t1,'Module':'AMASSS_CBCT Segmentation of T1','Display':DisplayAMASSS(nb_scan,len(full_seg_struct),len(full_reg_struct),False)})
            list_process.append({'Process':AMASSSProcess,'Parameter':parameter_amasss_seg_t2,'Module':'AMASSS_CBCT Segmentation of T2','Display':DisplayAMASSS(nb_scan,len(full_seg_struct),len(full_reg_struct))})
        
        return list_process


class Auto_CBCT(Semi_CBCT):

    def getTestFileList(self):
        return ("Fully-Automated", "https://github.com/lucanchling/Areg_CBCT/releases/download/TestFiles/Test_Full_AREG.zip")
        
    def TestScan(self, scan_folder_t1: str, scan_folder_t2: str):
        return super().TestScan(scan_folder_t1, scan_folder_t2, liste_keys = ['scanT1','scanT2'])

    def Process(self, **kwargs):

        list_struct = self.CheckboxisChecked(kwargs['dic_checkbox'])
        
        full_reg_struct = list_struct['Registration Type']
        reg_struct = self.TranslateModels(full_reg_struct, True)
        
        nb_scan = self.NumberScan(kwargs['input_t1_folder'], kwargs['input_t2_folder'])
        
        # AMASSS PROCESS - MASK SEGMENTATIONS        
        parameter_amasss_mask_t1 = {"inputVolume": kwargs['input_t1_folder'],
                                "modelDirectory": kwargs['model_folder_1'],
                                "highDefinition": False,
                                "skullStructure": reg_struct,
                                "merge": "SEPARATE",
                                "genVtk": False,
                                "save_in_folder": False,
                                "output_folder": kwargs['input_t1_folder'],
                                "precision": 50,
                                "vtk_smooth": 5,
                                "prediction_ID": 'Pred',
                                "gpu_usage": self.getGPUUsage(),
                                "cpu_usage": 1,
                                "temp_fold" : self.tempAMASSS_folder,
                                "SegmentInput" : False,
                                "DCMInput": False,
        }
        parameter_amasss_mask_t2 = {"inputVolume": kwargs['input_t2_folder'],
                                "modelDirectory": kwargs['model_folder_1'],
                                "highDefinition": False,
                                "skullStructure": reg_struct,
                                "merge": "SEPARATE",
                                "genVtk": False,
                                "save_in_folder": False,
                                "output_folder": kwargs['input_t2_folder'],
                                "precision": 50,
                                "vtk_smooth": 5,
                                "prediction_ID": 'Pred',
                                "gpu_usage": self.getGPUUsage(),
                                "cpu_usage": 1,
                                "temp_fold" : self.tempAMASSS_folder,
                                "SegmentInput" : False,
                                "DCMInput": False,
        }
        AMASSSProcess = slicer.modules.amasss_cli
        list_process = [{'Process':AMASSSProcess,'Parameter':parameter_amasss_mask_t1, 'Module':'AMASSS_CBCT - Masks Generation for T1', 'Display': DisplayAMASSS(nb_scan, len(full_reg_struct))},
                        {'Process':AMASSSProcess,'Parameter':parameter_amasss_mask_t2, 'Module':'AMASSS_CBCT - Masks Generation for T2', 'Display': DisplayAMASSS(nb_scan, len(full_reg_struct))},
        ]

        # print('AMASSS Mask Parameters:', parameter_amasss_mask_t1)
        # print()

        # AREG CBCT PROCESS
        full_reg_struct = list_struct['Registration Type']
        reg_struct = self.TranslateModels(full_reg_struct, False)
        
        AREGProcess = slicer.modules.areg_cbct
        for i,reg in enumerate(reg_struct.split(' ')):
            parameter_areg_cbct = {
                        't1_folder':kwargs['input_t1_folder'],
                        't2_folder':kwargs['input_t2_folder'],
                        'reg_type':reg,
                        'output_folder':kwargs['folder_output'],
                        'add_name':kwargs['add_in_namefile'],
                    }
            list_process.append({'Process':AREGProcess,'Parameter':parameter_areg_cbct,'Module':'AREG_CBCT for {}'.format(full_reg_struct[i]),'Display': DisplayAREGCBCT(nb_scan)})

        full_seg_struct = list_struct['AMASSS Segmentation']
        seg_struct = self.TranslateModels(full_seg_struct, False)

        # AMASSS PROCESS - SEGMENTATIONS
        AMASSSProcess = slicer.modules.amasss_cli
        parameter_amasss_seg_t1 = {"inputVolume": kwargs['input_t1_folder'],
                                "modelDirectory": kwargs['model_folder_1'],
                                "highDefinition": False,
                                "skullStructure": seg_struct,
                                "merge": "MERGE" if kwargs['merge_seg'] else "SEPARATE",
                                "genVtk": True,
                                "save_in_folder": False,
                                "output_folder": kwargs['folder_output'],
                                "precision": 50,
                                "vtk_smooth": 5,
                                "prediction_ID": 'Pred',
                                "gpu_usage": self.getGPUUsage(),
                                "cpu_usage": 1,
                                "temp_fold" : self.tempAMASSS_folder,
                                "SegmentInput" : False,
                                "DCMInput": False,
        }        
        parameter_amasss_seg_t2 = {"inputVolume": kwargs['folder_output'],
                                "modelDirectory": kwargs['model_folder_1'],
                                "highDefinition": False,
                                "skullStructure": seg_struct,
                                "merge": "MERGE" if kwargs['merge_seg'] else "SEPARATE",
                                "genVtk": True,
                                "save_in_folder": False,
                                "output_folder": kwargs['folder_output'],
                                "precision": 50,
                                "vtk_smooth": 5,
                                "prediction_ID": 'Pred',
                                "gpu_usage": self.getGPUUsage(),
                                "cpu_usage": 1,
                                "temp_fold" : self.tempAMASSS_folder,
                                "SegmentInput" : False,
                                "DCMInput": False,
        }
        if len(full_seg_struct) > 0:
            list_process.append({'Process':AMASSSProcess,'Parameter':parameter_amasss_seg_t1,'Module':'AMASSS_CBCT Segmentation for T1','Display':DisplayAMASSS(nb_scan,len(full_seg_struct))})
            list_process.append({'Process':AMASSSProcess,'Parameter':parameter_amasss_seg_t2,'Module':'AMASSS_CBCT Segmentation for T2','Display':DisplayAMASSS(nb_scan,len(full_seg_struct),len(full_reg_struct))})

        display = {'AMASSS_CBCT_MASK':DisplayAMASSS(nb_scan, len(full_reg_struct)),
                   'AMASSS_CBCT':DisplayAMASSS(nb_scan, len(full_seg_struct),len(full_reg_struct)),
                   'AREG_CBCT':DisplayAREGCBCT(nb_scan),
        }
        return list_process
        
        
    