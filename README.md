# IronCastBot
This is my college conclusion work. It's a way to evaluate ductile iron castings based on optical microscopy images. A graphical interface was developed using TKinter, and image processing was done using OpenCv.

# Features
Analysis of nodularity percentage, density per mm2, and nodules distribution by size class for optical microscopy of ductile iron following ASTM A247 16a and E2567 16a standards.

# Technologies Used
Python, Image Processing, Tesseract OCR, Tkinter, ImageDataExtractor.

# References
This project utilized the [ImageDataExtractor](https://github.com/by256/imagedataextractor) package, which in turn employs Tesseract 4 for optical character recognition, so it's necessary download it, [here](https://tesseract-ocr.github.io/tessdoc/Installation.html) contains a tutorial.

B. Yildirim, J. M. Cole, "Bayesian Particle Instance Segmentation for Electron Microscopy Image Quantification", J. Chem. Inf. Model. (2021) https://doi.org/10.1021/acs.jcim.0c01455

K. T. Mukaddem, E. J. Beard, B. Yildirim, J. M. Cole, "ImageDataExtractor: A Tool to Extract and Quantify Data from Microscopy Images", J. Chem. Inf. Model. (2019) https://doi.org/10.1021/acs.jcim.9b00734

# Installation
Python 3.7.8 was used and it is recommended to create a virtual environment. 
So if you want:
1. Clone the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Create a virtual environment for the project:
```
python -m venv ironcastbot_env
```
4. Activate the virtual environment:
```
<path>/ironcastbot_env/bin/activate.bat
```
5. Install the project dependencies:
```
pip install -r requirements.txt
```

# Usage
In your prompt with the virtual enviroment activate go to the directory and run InterfaceTkinter:
```
python InterfaceTkinter.py
```
So this window will show in screen:

![Screenshot of UI  of IronCastBot](https://dsm01pap007files.storage.live.com/y4mV3_AHbNOXDyE0HmbJSgR4ZS2bcHqhjF1pOgWDgcARtSQ6Bt6zyUPcFpTvdLpjtk4oIvZTX6zTKDISRGRGDI5vjf2ybIQGFaBRHfDEnWiEeF-bs8lejC2FxOxNjMlFxCKFwKLVkYyO_yZ8VGL1lJkbfw51KbabJGouSx0bdv_SRmAqIfqMmt4qMBP7MAISLE6R_BLydHESlS1I3uIX7hP-o2oboDi6PrMcRV0YyEwe6E?encodeFailures=1&width=763&height=511)

Initially, there is a listbox for inserting the directory or optical microscopy image. Choose the image and then adjust the threshold levels if necessary and press enter, particularly for the threshold of mask to remove the scale and possible voids or shrinkage defects, for example. 

If the image has a scale, click on clickbox for its detection and pixel/µm conversion.

If you are satisfied with the results, clicking on the "Run script" button will generate an "xlsx" file with data on percentage of nodularity, density, and distribution of nodules by size for all images in the folder or the desired image.

# Contributing
For the first version of this project, there was not a significant focus on the code architecture, processing, and UX. Therefore, there are improvements that can be implemented.

# License
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
