import tkinter as tk
from tkinter import messagebox
# module to check files
import os
import MainProcess
import cv2
from PIL import Image, ImageTk
import runScripForFiles
import ctypes
import base64
import io
class Win:
	def __init__(self, title, version):
		self.ImageProcessing = MainProcess.ProcessImage()
		self.runScript = runScripForFiles.RunScriptImageProcessing()
		self.root = tk.Tk()
		# self.ppi = self.root.winfo_fpixels("1i")
		self.ppi = ctypes.windll.user32.GetDpiForWindow(self.root.winfo_id()) 
		ic = "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"
		ic_data = base64.b64decode(ic)
		ic_buffer = io.BytesIO(ic_data)
		ic_image = Image.open(ic_buffer)
		ic_photo = ImageTk.PhotoImage(ic_image)
		self.root.title(f"{title}.{version}")
		# self.root.iconbitmap("source\Logo2.ico")
		self.root.iconphoto(True,ic_photo)
		hwnd = ctypes.windll.kernel32.GetConsoleWindow() 
		self.root.geometry("600x450")
		self.bluePurpleWorldColor = "#4258ff"
		self.smoothGrayPurple = '#dde'
		# Get the current screen width and height
		self.screen_width = int(self.root.winfo_screenwidth()*0.66)
		self.screen_height = int(self.root.winfo_screenheight()*0.75)
		self.lastSelectedIndex = ""
		self.lastdirectory = ""
		self.root.update_idletasks() # atualiza as dimensões da janela
		x = int(self.root.winfo_screenwidth()//2 - self.screen_width//2)
		y = int(self.root.winfo_screenheight()//2 - self.screen_height//2)
		self.root.geometry(f"{self.screen_width}x{self.screen_height}+{x}+{y}")
		self.CreatedBy = "iVBORw0KGgoAAAANSUhEUgAAAKcAAAAjCAMAAADG6eoQAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAA2UExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALd2aHIAAAARdFJOUwATIi88SktYZ3aFlqi4y9zugwSdbwAAAAlwSFlzAAAXEQAAFxEByibzPwAAAi5JREFUWEftlItu5CAMRQ04S3gY8P//7F4TplVnqzbqatVKy1GUEMaPG9sMbTabzWaz+SYkr8UHZAkU7hj+JY497p7d9foGlbX4AFEmvmP4BWJaC8BqLwnZ/uS7dYquBfhcJyfGl3niItmRS1Jhy1XO2YIXnUetBwKlIOVhdZ5mcYtYS6AUU7GVN//sfNdIPktE2HounacclA4K6RcGzuC4dCZYQI1XIFTs4dnuxX596Dxs5yDVodMe+KT1vXF6hwi3AWcth/bRKatoRRKhpk1j0DGWzj7U10Z58FXajP03OpMWh/Pio8OnJT1cmXYPnaIhaEWqEPGmwxVFaXWgxjeo6jg67Q51gOhAnmQgJnkk7xXpjqWTo12+1ennm6LHTzqnLncmKMD3l7d9FxMPgTrfcJlbGhbmBtckWj5RacrcUFvbZe0yBLlf5hN1dJowEZNzoBLm96xzdjRRRKD566tO8KQTXZo+nwNF+B6LiHjMrrejLZ2FOTzpRPnV/qUM3x59jw+dkaInbfCFTnIIBKpto+FWEQz2Q2ebOu+OJ4xz687ywa0KjcpdMXsnIp0dTa916axWmIj4YZ0jZNUhIpl1ZLWhGKIde6lpymgHBh9EVFGhtahYqKWzqwyNd1VimhAjz7pcq2wHh3gIxaE9oCZICruEZ4MRTNY5MqyV8BVtGBn42qnAHXos2uopNuA14zeU+9IZ+tz8V4RXjT+ZdLXyxxPxX7/ZbDabzf8C0W8wayJky2NAJQAAAABJRU5ErkJggg=="
		self.window()
		# self.root.eval('tk::PlaceWindow . center')

	def window(self):
		"Contains all the widgets"
		# frame in left side in window
		def frame():
			"Contains the list of chapter names in listbox"
			self._frame = tk.Frame(self.root, bg=self.bluePurpleWorldColor,width=self.screen_width*0.15)
			# self._frame.grid(column=0, row=0,
			# sticky="nswe") # adapt the fram to the window
			self._frame.pack(ipadx=5, ipady=10, fill=tk.BOTH, side=tk.LEFT)
		
		# Region widgets in frame of leftside
		def listbox():
			"The book chapter name list goes here"
			# self._lbx = tk.Listbox(self._frame, bg="yellow")
			self._lbx = tk.Listbox(self._frame, bg=self.smoothGrayPurple,width=int(self.screen_width*0.05))
			# self._lbx.grid(column=0, row=1, sticky="n") # adapt the listbox to the frame
			self._lbx.pack(fill=tk.Y, expand=True)

		def listBoxEvents():
			try:
				def on_focus_out(event):
					self._lbx.selection_set(self.lastSelectedIndex)

				self._lbx.bind("<<ListboxSelect>>",
					lambda x: showimage(
					self.textBox.get(),
					self._lbx.get(self._lbx.curselection())))
				
				self._lbx.bind("<FocusOut>", on_focus_out)
			except:
				showimage(
					self.textBox.get(),
					self.lastSelectedIndex)

		def update_selected_index():
			# armazena o índice do arquivo selecionado
			self.selected_index = self._lbx.curselection()
			lambda x: showimage(
					self.textBox.get(),
					self._lbx.get(self._lbx.curselection()))

		def reset_selection():
			# define a seleção do arquivo selecionado novamente quando o foco retorna à janela
			if self.selected_index is not None:
				self._lbx.selection_set(self.selected_index)

		def showimage(directory, fileImage = ""):
			if(directory.lower().endswith((".png", ".jpeg", ".jpg", ".bitmap"))):
				filename = directory
				self.lastSelectedIndex = filename
			else:
				if directory!="" and fileImage!="":
					filename = os.path.join(directory, fileImage)
					self.lastSelectedIndex = filename
			# fp = os.path.abspath(directory+fileImage)
			if(fileImage=="" and directory==""):
				filename = self.lastSelectedIndex
			if(self.lastSelectedIndex==""):
				messagebox.showwarning("Warning","Please select a item image!")
				return
			try:
				self.img = Image.open(filename)
			except Exception as e:
				messagebox.showerror("Error","Error to read image, make sure the file path is correct. ")
			self.ratioConversionSize = int(self.screen_height*0.5)/self.img.size[1]
			self.widthResize = int(self.ratioConversionSize * self.img.size[0])
			self.resized_image= self.img.resize((self.widthResize,int(self.screen_height*0.5)), Image.ANTIALIAS)
			self.resized_image = ImageTk.PhotoImage(self.resized_image)
			self.image = self.resized_image
			self._labInput["image"] = self.resized_image
			showimageOutput(filename)

		def additems(directory=''):
			if directory == '': return
			if(directory!=self.lastdirectory and self.lastdirectory!=""):
				self._lbx.delete(0, tk.END)
			self.lastdirectory = directory
			if(directory.endswith((".png", ".jpeg", ".jpg"))):
				self._lbx.insert("anchor",os.path.basename(directory))
				listBoxEvents()
				return
			for file in os.listdir(directory):
				if file.lower().endswith((".png", ".jpeg", ".jpg")):
					if not file in self._lbx.get(0,"end"):
						self._lbx.insert("anchor", file)
			listBoxEvents()

		def textBoxDirectory():
			self.labelDirectory = tk.Label(self._frame,text="File Image or path (press enter):",bg=self.bluePurpleWorldColor,foreground="#ffffff")
			self.labelDirectory.pack(side='top',anchor=tk.N,fill="x")
			self.textBox = tk.Entry(self._frame,background=self.smoothGrayPurple,foreground="black",width=int(self.screen_width*0.05))
			self.textBox.pack(side='top',anchor=tk.N)
			self.textBox.bind("<Return>", lambda x: additems(self.textBox.get()))
		
		
		def frameThreshold():
			self.frameThr = tk.Frame(self._frame,bg=self.smoothGrayPurple,width=int(self.screen_width*0.05),height=int(self.screen_height*0.2))
			self.frameThr.pack(fill="x",ipadx=5,padx=5)

		def checkBoxScaleBarDetection():			
			self.ScaleBarDetection_checked = tk.BooleanVar(value=False)
			self.checkButtonAllFiles = tk.Checkbutton(self.frameThr,text="Scalebar Detection",onvalue=True,offvalue=False,variable=self.ScaleBarDetection_checked,bg=self.smoothGrayPurple)
			self.checkButtonAllFiles.pack(anchor=tk.W)
			# self.checkButtonAllFiles.bind("<Button-1>",lambda x:showimage(self.lastSelectedIndex))
			self.ScaleBarDetection_checked.trace_add("write", lambda *args: handle_checkbutton_change())

		def handle_checkbutton_change():
				showimage(self.lastSelectedIndex)

		def ThresholdMaskWidgets():
			self.frameThresholdMask = tk.Frame(self.frameThr,bg=self.smoothGrayPurple,width=int(self.screen_width*0.05))
			self.frameThresholdMask.pack(anchor=tk.W,expand=True,fill="x",ipadx=5)
			self.labelThresholdMask = tk.Label(self.frameThresholdMask, text='Threshold Mask (default:45-255):' )
			self.labelThresholdMask.pack(anchor='w')
			self.frameThresholdMaskMin = tk.Frame(self.frameThresholdMask,bg=self.smoothGrayPurple,width=int(self.screen_width*0.05))
			self.frameThresholdMaskMin.pack(anchor=tk.W,fill=tk.X)
			self.labelMinThresholdMask = tk.Label(self.frameThresholdMaskMin, text='Min:',justify=tk.LEFT )
			self.labelMinThresholdMask.pack(side=tk.LEFT,fill="x")
			self.entryMinThresholdMask = tk.Entry(self.frameThresholdMaskMin)
			self.entryMinThresholdMask.pack(side=tk.RIGHT, expand=True,fill="x")
			self.frameThresholdMaskMax = tk.Frame(self.frameThresholdMask,bg=self.smoothGrayPurple,width=int(self.screen_width*0.05))
			self.frameThresholdMaskMax.pack(anchor=tk.W,fill=tk.X)
			self.labelMaxThresholdMask = tk.Label(self.frameThresholdMaskMax, text='Max:' )
			self.labelMaxThresholdMask.pack(side=tk.LEFT)
			self.entryMaxThresholdMask = tk.Entry(self.frameThresholdMaskMax)
			self.entryMaxThresholdMask.pack(side=tk.RIGHT,expand=True,fill=tk.X)

			self.entryMinThresholdMask.bind("<Return>",
				lambda x: showimage(
				self.lastSelectedIndex))
			self.entryMaxThresholdMask.bind("<Return>",
				lambda x: showimage(
				self.lastSelectedIndex))

		def ThresholdWidgetsOtsu():
			self.frameThreshold2 = tk.Frame(self.frameThr,bg=self.smoothGrayPurple,width=int(self.screen_width*0.05))
			self.frameThreshold2.pack(anchor=tk.W,expand=True,fill="x",ipadx=5)
			self.labelThreshold2 = tk.Label(self.frameThreshold2, text='Threshold image process (default:OTSU):' )
			self.labelThreshold2.pack(anchor='w')
			self.frameThresholdMin2 = tk.Frame(self.frameThreshold2,bg=self.smoothGrayPurple,width=int(self.screen_width*0.05))
			self.frameThresholdMin2.pack(anchor=tk.W,fill=tk.X)
			self.labelMinThreshold2 = tk.Label(self.frameThresholdMin2, text='Min:',justify=tk.LEFT )
			self.labelMinThreshold2.pack(side=tk.LEFT,fill="x")
			self.entryMinThresholdOtsu = tk.Entry(self.frameThresholdMin2)
			self.entryMinThresholdOtsu.pack(side=tk.RIGHT, expand=True,fill="x")
			self.frameThresholdMax2 = tk.Frame(self.frameThreshold2,bg=self.smoothGrayPurple,width=int(self.screen_width*0.05))
			self.frameThresholdMax2.pack(anchor=tk.W,fill=tk.X)
			self.labelMaxThreshold2 = tk.Label(self.frameThresholdMax2, text='Max:' )
			self.labelMaxThreshold2.pack(side=tk.LEFT)
			self.entryMaxThresholdOtsu = tk.Entry(self.frameThresholdMax2)
			self.entryMaxThresholdOtsu.pack(side=tk.RIGHT,expand=True,fill=tk.X)

			self.entryMinThresholdOtsu.bind("<Return>",
				lambda x: showimage(
				self.lastSelectedIndex))
			self.entryMaxThresholdOtsu.bind("<Return>",
				lambda x: showimage(
				# self.textBox.get(),
				self.lastSelectedIndex))
		# end 

		# Frame in the middle window (contains images widgets)
		def frame2():
			"Contains the text"
			self._frame2 = tk.Frame(self.root, bg=self.smoothGrayPurple)
			self._frame2.pack(ipadx=5, ipady=5, side=tk.LEFT,expand=True,fill=tk.BOTH)
			self.height_frame2 = self._frame2.winfo_height();
			# self._frame2.grid(column=1, row=0,rowspan=1)

		# def text():
		# 	"Contains the text of selected chapter in listbox"
		# 	self._text = tk.Text(self._frame2)
		# 	self._text.grid(column=1, row=1)
			
		
		def labelInputImg():
			"Contains the text of selected chapter in listbox"
			self._labInput = tk.Label(self._frame2,height=int(self.height_frame2*0.5))
			self._labInput.grid(column=0, row=0)

		
		def showimageOutput(fileImage):
			self.img = cv2.imread(r"%s"%fileImage,0)
			self.imageReturn, blobCount ,self.ShapeFactorAchieve, self.nodularity,self.density,self.text,self.RatioPixel ,_ = self.ImageProcessing.InputImg(
				self.img, self.ppi,self.ScaleBarDetection_checked.get(),
				self.entryMinThresholdMask.get(), self.entryMaxThresholdMask.get(),self.entryMinThresholdOtsu.get(),self.entryMaxThresholdOtsu.get())
			self.imgPill = Image.fromarray(self.imageReturn)
			self.ratioConversionSize = int(self.screen_height*0.5)/self.imgPill.size[1]
			self.widthResize = int(self.ratioConversionSize * self.imgPill.size[0])
			self.resized_image= self.imgPill.resize((self.widthResize,int(self.screen_height*0.5)), Image.ANTIALIAS)
			self.imgOutput = ImageTk.PhotoImage(self.resized_image)
			self.image2 = self.imgOutput
			self._labOutput.configure(image = self.imgOutput)
			self.TotalBlobsValue['text'] = blobCount
			self.TotalNodulesValue['text'] = self.ShapeFactorAchieve
			self.NodularityValue['text'] = self.nodularity
			self.ScaleBarDetectedValue['text'] = self.text
			self.DensityValue['text'] = self.density
			self.ScaleBarDetectedConversionValue['text'] = self.RatioPixel

		def labelOutputImg():
			"Contains the text of selected chapter in listbox"
			self._labOutput = tk.Label(self._frame2,height=int(self.height_frame2*0.5))
			self._labOutput.grid(column=0, row=1)

		#  frame in right side in windows
		def PanelFrame3():
			self.frame3 = tk.Frame(self.root,width=self.screen_width*0.15,bg=self.smoothGrayPurple,height=self.screen_height)
			self.frame3.pack(fill='both',ipadx=5, ipady=5, side=tk.RIGHT,anchor="ne",expand=True)
			self.widthFrame3 = self.frame3.winfo_width()
			self.fullScreenFrame = tk.Frame(self.frame3, bg=self.smoothGrayPurple)
			self.fullScreenFrame.pack(fill='both', expand=True)

		def WidsLabelsInfos():
			self.frameWidsLabel = tk.Frame(self.fullScreenFrame,width=self.widthFrame3,bg=self.smoothGrayPurple,pady=20)
			self.frameWidsLabel.pack(in_=self.fullScreenFrame, side=tk.TOP, fill='both', padx=15)
			framePanelBlobs = tk.Frame(self.frameWidsLabel,width=self.widthFrame3,bg='#fafafa')
			framePanelBlobs.pack(anchor='nw',fill=tk.X,padx=5)
			self.labelCountBlobs = tk.Label(framePanelBlobs,text="Nodules with minimum size:",bg='#fafafa')
			self.labelCountBlobs.pack(anchor=tk.W,side=tk.LEFT)
			self.TotalBlobsValue = tk.Label(framePanelBlobs,text="",anchor='e',bg='#fafafa')
			self.TotalBlobsValue.pack(anchor=tk.W,side=tk.LEFT,fill='x')
			
			framePanelNodules = tk.Frame(self.frameWidsLabel,width=self.widthFrame3,bg='#cecede')
			framePanelNodules.pack(anchor='nw',fill=tk.X,padx=5)
			self.labelCountNodules = tk.Label(framePanelNodules,text="Total nodules:",bg='#cecede')
			self.labelCountNodules.pack(anchor=tk.W,side=tk.LEFT)
			self.TotalNodulesValue = tk.Label(framePanelNodules,text="",bg='#cecede')
			self.TotalNodulesValue.pack(anchor=tk.W,side=tk.LEFT,fill='x')

			framePanelNodularity = tk.Frame(self.frameWidsLabel,width=self.widthFrame3,bg='#fafafa')
			framePanelNodularity.pack(anchor='nw',fill=tk.X,padx=5)
			self.Nodularity = tk.Label(framePanelNodularity,text="Nodularity:",bg='#fafafa')
			self.Nodularity.pack(anchor=tk.W,side=tk.LEFT)
			self.NodularityValue = tk.Label(framePanelNodularity,text="",bg='#fafafa')
			self.NodularityValue.pack(anchor=tk.W,side=tk.LEFT,fill='x')

			framePanelDensity= tk.Frame(self.frameWidsLabel,width=self.widthFrame3,bg='#cecede')
			framePanelDensity.pack(anchor='nw',fill=tk.X,padx=5)
			self.Density = tk.Label(framePanelDensity,text="Density per mm2:",bg='#cecede')
			self.Density.pack(anchor=tk.W,side=tk.LEFT)
			self.DensityValue = tk.Label(framePanelDensity,text="",bg='#cecede')
			self.DensityValue.pack(anchor=tk.W,side=tk.LEFT,fill='x')

			framePanelScale = tk.Frame(self.frameWidsLabel,width=self.widthFrame3,bg='#fafafa')
			framePanelScale.pack(anchor='nw',fill=tk.X,padx=5)
			self.ScaleBar = tk.Label(framePanelScale,text="Scalebar detected:",bg='#fafafa')
			self.ScaleBar.pack(anchor=tk.W,side=tk.LEFT)
			self.ScaleBarDetectedValue = tk.Label(framePanelScale,text="",bg='#fafafa')
			self.ScaleBarDetectedValue.pack(anchor=tk.W,side=tk.LEFT,fill='x')

			framePanelScaleConvertion = tk.Frame(self.frameWidsLabel,width=self.widthFrame3,bg='#cecede')
			framePanelScaleConvertion.pack(anchor='nw',fill=tk.X,padx=5)
			self.ScaleBar = tk.Label(framePanelScaleConvertion,text="Conversion:",bg='#cecede')
			self.ScaleBar.pack(anchor=tk.W,side=tk.LEFT)
			self.ScaleBarDetectedConversionValue = tk.Label(framePanelScaleConvertion,text="",bg='#cecede')
			self.ScaleBarDetectedConversionValue.pack(anchor=tk.W,side=tk.LEFT,fill='x')

		def runScript():
				self.runScript.MinThresholdMask = self.entryMinThresholdMask.get()
				self.runScript.MaxThresholdMask = self.entryMaxThresholdMask.get()
				self.runScript.MinThresholdProcess = self.entryMinThresholdMask.get()
				self.runScript.MaxThresholdProcess = self.entryMaxThresholdMask.get()
				if self.allfiles_checked.get():
					self.runScript.input(self.textBox.get(), self.ppi,self.ScaleBarDetection_checked.get(),
				self.entryMinThresholdMask.get(), self.entryMaxThresholdMask.get(),self.entryMinThresholdOtsu.get(),self.entryMaxThresholdOtsu.get())
				else:
					self.runScript.input(self.lastSelectedIndex,self.ppi,self.ScaleBarDetection_checked.get(), self.entryMinThresholdMask.get(), self.entryMaxThresholdMask.get(),self.entryMinThresholdOtsu.get(),self.entryMaxThresholdOtsu.get())

		def PanelWidgetsRunScript():
			frameParent = tk.Frame(self.fullScreenFrame,bg=self.smoothGrayPurple,pady=20,padx=15)
			frameParent.pack(fill='both')
			self.allfiles_checked = tk.BooleanVar()
			self.checkButtonAllFiles = tk.Checkbutton(frameParent,text="All files in path",onvalue=True,offvalue=False,variable=self.allfiles_checked,bg=self.smoothGrayPurple)
			self.checkButtonAllFiles.pack(anchor=tk.E)
			buttonScript = tk.Button(frameParent,text="Run Script",command=runScript,bg=self.bluePurpleWorldColor,padx=15,pady=5,foreground="#ffffff")
			buttonScript.pack(anchor=tk.E)

		def CreatedBy():
			frameParent = tk.Frame(self.fullScreenFrame,bg=self.smoothGrayPurple,pady=5,padx=10)
			frameParent.pack(in_=self.fullScreenFrame, side=tk.RIGHT, anchor='se', padx=5, pady=5)
			createdBy = tk.PhotoImage(data=base64.b64decode(self.CreatedBy))
			label = tk.Label(frameParent, image=createdBy,bg=self.smoothGrayPurple, height=10,width=90)
			label.image = createdBy  # Mantenha uma referência à imagem para evitar que ela seja coletada pelo garbage collector
			label.configure(width=createdBy.width(), height=createdBy.height())
			label.pack(anchor=tk.S)

		def widgets_order():
			"The widgets on the screen"
			frame()
			textBoxDirectory()
			listbox()
			frameThreshold()
			checkBoxScaleBarDetection()
			ThresholdMaskWidgets()
			ThresholdWidgetsOtsu()
			frame2()
			labelInputImg()
			labelOutputImg()
			PanelFrame3()
			WidsLabelsInfos()
			PanelWidgetsRunScript()
			CreatedBy()

		widgets_order()

# ================ main ============
if __name__ == "__main__":
	ver = "1.0"
	win = Win("IronCastBot", ver)
	win.root.mainloop()