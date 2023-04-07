import pandas as pd
import os
import MainProcess
from glob import glob
import cv2
from pathlib import Path
from datetime import datetime

class RunScriptImageProcessing:
    MinThresholdMask = None
    MaxThresholdMask = None
    MinThresholdProcess = None
    MaxThresholdProcess = None
    def __init__(self) -> None:
        self.filePathXlsx = ''
        self.ImageProcessing = MainProcess.ProcessImage()
        pass

    def input(self, filepath,ppi,flagScaleBar,minThresholdMask = '',maxThresholdMask = '',minThrOtsu = '', maxThrOtsu = ''):
        self.data = {
            'FileImage': [],
            'Nodularity':[],
            'Nodules Count':[],
            'Density nodules': [],
            "ScaleBar":[],
            "Conversion":[],
            '<_20': [],
            '20_<40': [],
            '40_<80': [],
            '80_<160': [],
            '160_<320': [],
            '320_<640': [],
            '640_<1280': [],
            '>_1280': []
        }
        types = ('.png', '.jpeg','.jpg')

        files_grabbed = []

        if filepath.lower().endswith(types):
            files_grabbed.extend(glob(filepath))
            self.filePathXlsx = filepath.split('.')[0]+".xlsx"
        else:
            parentPath = Path(filepath)
            filename = f"process_{str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}.xlsx"
            self.filePathXlsx = os.path.join(parentPath,filename)
            for filesTypes in types:
                files_grabbed.extend(glob(filepath ,* filesTypes))

        for file in files_grabbed:
            img = cv2.imread(file,0)
            imageReturn, blobCount ,nodulesCount, nodularity, density, scaleBar,scaleBarValue, dict_distribuition = self.ImageProcessing.InputImg(img,
            ppi, flagScaleBar, minThresholdMask ,maxThresholdMask ,minThrOtsu , maxThrOtsu )
            self.data['FileImage'].append(os.path.basename(filepath))
            self.data['Nodularity'].append(nodularity)
            self.data["Nodules Count"].append(nodulesCount)
            self.data['Density nodules'].append(density)
            self.data['ScaleBar'].append(scaleBar)
            self.data["Conversion"].append(scaleBarValue)
            self.data['<_20'].append(dict_distribuition['<_20']),
            self.data['20_<40'].append(dict_distribuition['20_<40'])
            self.data['40_<80'].append(dict_distribuition['40_<80'])
            self.data['80_<160'].append(dict_distribuition['80_<160'])
            self.data['160_<320'].append(dict_distribuition['160_<320'])
            self.data['320_<640'].append(dict_distribuition['320_<640'])
            self.data['640_<1280'].append(dict_distribuition['640_<1280'])
            self.data['>_1280'].append(dict_distribuition['>_1280'])

        df = pd.DataFrame(self.data)
        df.to_excel(self.filePathXlsx)
        return