#!/usr/bin/env python-real
import argparse
import sys,os,time
import numpy as np
import slicer
from slicer.util import pip_install,pip_uninstall
pip_install('SimpleITK-SimpleElastix -q')
import SimpleITK as sitk

fpath = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(fpath)

from AREG_CBCT_utils import GetDictPatients, VoxelBasedRegistration, LoadOnlyLandmarks, applyTransformLandmarks, WriteJson, translate 

def main(args):

    t1_folder, t2_folder, output_dir, reg_type, add_name = args.t1_folder[0], args.t2_folder[0], args.output_folder[0], args.reg_type[0], args.add_name[0]

    patients = GetDictPatients(t1_folder,t2_folder,segmentationType=reg_type)
    
    for patient,data in patients.items():
        
        transform, resample_t2, resample_t2_seg = VoxelBasedRegistration(data['scanT1'],data['scanT2'],data['segT1'],data['segT2'],approx=True)
        
        outpath = os.path.join(output_dir,translate(reg_type),patient+'_OutReg')
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        sitk.WriteTransform(transform, os.path.join(outpath,patient+'_'+reg_type+add_name+'_matrix.tfm'))
        sitk.WriteImage(resample_t2, os.path.join(outpath,patient+'_'+reg_type+add_name+'.nii.gz'))
        sitk.WriteImage(resample_t2_seg, os.path.join(outpath,patient+'_'+reg_type+'MASK_'+add_name+'.nii.gz'))
        # if args.reg_lm:   
        #     transformedLandmarks = applyTransformLandmarks(LoadOnlyLandmarks(data['lmT2']), transform.GetInverse())
        #     WriteJson(transformedLandmarks, os.path.join(outpath,patient+'_lm_'+add_name+'.mrk.json'))
        
        print(f"""<filter-progress>{0}</filter-progress>""")
        sys.stdout.flush()
        time.sleep(0.2)
        print(f"""<filter-progress>{2}</filter-progress>""")
        sys.stdout.flush()
        time.sleep(0.2)
        print(f"""<filter-progress>{0}</filter-progress>""")
        sys.stdout.flush()
        time.sleep(0.2)
        
if __name__ == "__main__":
    
    print("PRE ASO")

    parser = argparse.ArgumentParser()

    parser.add_argument('t1_folder',nargs=1)
    parser.add_argument('t2_folder',nargs=1)
    parser.add_argument('reg_type',nargs=1)
    parser.add_argument('output_folder',nargs=1)
    parser.add_argument('add_name',nargs=1)
    # parser.add_argument('reg_lm',nargs=1)

    args = parser.parse_args()
    
    main(args)