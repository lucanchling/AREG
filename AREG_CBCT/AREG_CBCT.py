#!/usr/bin/env python-real

import argparse
import SimpleITK as sitk
import sys,os,time
import numpy as np
import slicer

fpath = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(fpath)

from AREG_CBCT_utils import (ExtractFilesFromFolder, DenseNet, AngleAndAxisVectors, RotationMatrix, PreASOResample)

def main(args):

    input_dir, out_dir = args.input[0], args.output_folder[0]

    for i in range(10):
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
    parser.add_argument('reg_lm',nargs=1)

    args = parser.parse_args()
    
    main(args)