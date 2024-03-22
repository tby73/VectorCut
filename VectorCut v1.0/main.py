import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

from vectorcut import VectorCut

DXF_SAVE_TIME = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DXF_DIR = "VC_DXF_OUT/"
OUTPUT_DXF = f"{OUTPUT_DXF_DIR}/dxf_{DXF_SAVE_TIME}.dxf"

def main():
    # create output dir if it doesnt exist
    if not os.path.exists(OUTPUT_DXF_DIR):
        os.mkdir(OUTPUT_DXF_DIR)

    bmp_path = input("VECTORCUT/BITMAPPATH> ")
    bmp_input = cv2.cvtColor(cv2.imread(bmp_path), cv2.COLOR_BGR2RGB)
    vector_cut = VectorCut(bmp_input, OUTPUT_DXF)
    
    contour_img = vector_cut.DisplayContours()
    contour_plane = vector_cut.ExtractContourImage()
    
    vector_cut.DisplayCut([contour_img, contour_plane])
    vector_cut.Convert2DXF()

if __name__ == "__main__":
    main()

