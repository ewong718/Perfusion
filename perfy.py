'''
Perfy Perfusion MRI Data Analyzer
Updated on June 23, 2014

@author: edmundwong
'''

from Tkinter import StringVar
import Tkinter
import tkFileDialog
import os
import nibabel.nifti1
import tkMessageBox

fslPerfScriptPath="/Users/edmundwong/Documents/workspace/PerfusionGUIPy/core/python_fsl.sh"

class Perfusion_gui(Tkinter.Tk):
    
    fileselected = False
     
    def __init__(self): 
        Tkinter.Tk.__init__(self)         
        self.initialize()
        
    def initialize(self):
        Tkinter.Label(self, text="Perfy v1.0", anchor="center",fg="white",bg="DodgerBlue", padx="25", pady="5").grid(column=0,row=0,columnspan=3,sticky='EW')
        Tkinter.Button(self, text="Select File", command= self.open_file_dialog).grid(column=0,row=1,columnspan=1,sticky='EW')
        Tkinter.Label(self, text="Start vol", anchor="e",fg="black",bg="white", pady="7").grid(column=1,row=1,columnspan=1,sticky='EW')
        self.entry_start = Tkinter.Entry(self, width=2)
        self.entry_start.grid(column=2,row=1,columnspan=1,sticky='EW')
        Tkinter.Label(self, text="End vol", anchor="e",fg="black",bg="white", pady="7").grid(column=1,row=2,columnspan=1,sticky='EW')
        self.entry_end = Tkinter.Entry(self, width=2)
        self.entry_end.grid(column=2,row=2,columnspan=1,sticky='EW')
        Tkinter.Button(self,text="R U N", command=self.process_data).grid(column=0,row=2,columnspan=1,sticky='EW')
        self.displaytext = StringVar()
        self.displaytext.set("Ready")
        Tkinter.Label(self, textvariable=self.displaytext, anchor="center",fg="white",bg="MediumVioletRed").grid(column=0,row=3,columnspan=3,sticky='EW')
        
    def open_file_dialog(self):
        # Load nifti header information
        self.filename = tkFileDialog.askopenfilename(filetypes=[('Nifti files', '.nii'), ('Nifti.gz files', '.gz')])
        try:
            img=nibabel.nifti1.load(self.filename)
        except nibabel.nifti1.ImageFileError:
            tkMessageBox.showerror("Error", "Not a valid nifti file.")
            return
        except IOError:
            return
        dims=img.get_shape()
        try:            
            self.volumes=dims[3]
        except IndexError:
            tkMessageBox.showerror("Error", "Not a multi-dimension nifti file.")
            return
        self.displaytext.set(self.filename)
        self.fileselected = True
    
    def process_data(self):
        if self.fileselected == False:
            tkMessageBox.showerror("Error", "You must select a nifti file first.")
            return        
        try:    
            startvol = int(self.entry_start.get())
        except ValueError:
            tkMessageBox.showerror("Error", "Start volume must be an integer.")
            return
        try:
            endvol = int(self.entry_end.get())
        except ValueError:
            tkMessageBox.showerror("Error", "End volume must be an integer.")
            return
        if startvol < 0:
            tkMessageBox.showerror("Error", "Start volume cannot be less than 0.")
            return        
        if endvol <= startvol:
            tkMessageBox.showerror("Error", "End volume cannot be less than or equal to start volume.")
            return
        if endvol > self.volumes:
            tkMessageBox.showerror("Error", "End volume value cannot be greater than number of actual volumes.")
            return
        os.system("bash " + fslPerfScriptPath + " " + self.filename + " " + str(startvol) + " " + str(endvol))
        tkMessageBox.showinfo("Complete", "Complete.")
        #os.system("echo Processed!")
             

if __name__ == '__main__':
    app = Perfusion_gui()
    app.title("Perfy")
    app.resizable(width="FALSE", height="FALSE")
    #app.geometry("500x300")
    app.mainloop()