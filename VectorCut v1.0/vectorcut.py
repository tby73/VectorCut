import cv2
import numpy as np
import matplotlib.pyplot as plt
import ezdxf as dxf

class VectorCut:
    def __init__(self, input_image, output_path) -> None:
        self.input_image = cv2.resize(input_image, (700, 600), interpolation=cv2.INTER_CUBIC)
        self.output_path = output_path
        self.DXF_VERSION = "R2010"
    
    def Preprocess(self):
        grayscaled = cv2.cvtColor(self.input_image, cv2.COLOR_RGB2GRAY)

        blured = cv2.GaussianBlur(grayscaled, (3, 3), 0)
        edges = cv2.Canny(blured, 255, 0)

        return edges
    
    def GetContours(self):
        preprocessed = self.Preprocess()
        contours, hierarchy = cv2.findContours(preprocessed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def DisplayContours(self):
        contours = self.GetContours()
        display_overlay = self.input_image.copy()
        cv2.drawContours(display_overlay, contours, -1, (0, 255, 0), 1, lineType=cv2.LINE_AA)
        return display_overlay
    
    def ExtractContourImage(self):
        self.extraction_plane = np.zeros(self.input_image.copy().shape)
        contours = self.GetContours()
        cv2.drawContours(self.extraction_plane, contours, -1, (0, 255, 0), 1, lineType=cv2.LINE_AA)
        return self.extraction_plane
    
    def Convert2DXF(self):
        contours = self.GetContours()
        contours_squeezed = [np.squeeze(cnt, axis=1) for cnt in contours]

        dxf_out = dxf.new(self.DXF_VERSION)
        msp = dxf_out.modelspace()
        dxf_out.layers.new(name="BITMAP_CONTOUR_LINES", dxfattribs={"color": 3})

        for contour in contours_squeezed:
            for n in range(len(contour)):
                if n >= len(contour) - 1:
                    n = 0
                try:
                    msp.add_line(contour[n], contour[n + 1], dxfattribs={"layer": "BITMAP_CONTOUR_LINES", "lineweight": 20}) 
                except IndexError:
                    pass       

        dxf_out.saveas(self.output_path)

    def DisplayCut(self, images: list):
        for i in range(len(images)):
            plt.subplot(1, 2, i + 1)
            plt.imshow(images[i])
            plt.title(f"CUT BMP - {i}")
            plt.ylabel("y")
            plt.xlabel("x")
        
        plt.show()
    


    
