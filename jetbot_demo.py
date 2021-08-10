#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pyrealsense2 as rs
import numpy as np
import time
import cv2
from tkinter import font as tkfont
import tkinter.filedialog
import tkinter as tk
import ast
import os
from tkinter.ttk import Progressbar
from PIL import Image
from PIL import ImageTk
#from PIL import ImageGrab
from jetbot import Robot


# In[3]:


class Scan(): 
    def __init__(self,width,height,framerate,autoexposureFrames):
       
        self.width = width
        self.height = height
        self.framerate = framerate
        #self.backDistance = backDistance
        self.autoexposureFrames = autoexposureFrames
        
        
        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.framerate)
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.any, self.framerate)
        
        #post-processing filters
        #depth representation and disparity representation transform
        self.depth_to_disparity =  rs.disparity_transform(True)
        self.disparity_to_depth = rs.disparity_transform(False)

    def startPipeline(self):
        self.intr = self.pipe.start(self.config)
        self.align = rs.align(rs.stream.color)
        print("pipeline start")
    
    def stopPipeline(self):
        self.pipe.stop()
        self.pipe = None
        self.config = None
        print("pipeline stop")
        
    def waitPhoto(self):
        print("wait photo !")
        for i in range(self.autoexposureFrames):
            self.frameset = self.pipe.wait_for_frames()
        
    def takePhoto(self):
        print("take photo !")
        # start
        self.frameset = self.pipe.wait_for_frames()
        self.frameset = self.align.process(self.frameset)
        self.profile = self.frameset.get_profile()
        
        self.color_intr = rs.video_stream_profile(self.intr.get_stream(rs.stream.color)).get_intrinsics()
        
        self.color_frame = self.frameset.get_color_frame()
        self.depth_frame = self.frameset.get_depth_frame()

        self.depth_image = np.asanyarray(self.depth_frame.get_data())
        self.color_image = np.asanyarray(self.color_frame.get_data())
    
    def giveImageArray(self):
        return self.color_image
    
    def giveDepthArray(self):
        return self.depth_image
    
    def getIntrinsics(self):
        return self.color_intr
    
    def Image_alignment(self):
        self.depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image, alpha=0.255), cv2.COLORMAP_JET)
        self.depth_colormap_dim = self.depth_colormap.shape
        self.color_colormap_dim = self.color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if self.depth_colormap_dim != self.color_colormap_dim:
            self.resized_color_image = cv2.resize(self.color_image, dsize=(self.depth_colormap_dim[1], self.depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            self.images = np.hstack((self.resized_color_image, self.depth_colormap))
        else:
            self.images = np.hstack((self.color_image, self.depth_colormap))
        
        return self.images
    
    def get3DPoint(self, u ,v):
        d = scan.depth_frame.get_distance(u, v)
        point = rs.rs2_deproject_pixel_to_point(self.color_intr, [u,v], d)
        return point


# In[23]:


class App(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.Height = 480
        self.Width = 1280
        self.title_font = tkfont.Font(family='Arial', size=18, weight="bold", slant="italic")
        self.title('Jetbot')
        self.geometry('1600x1000')
        self.canvas = tk.Canvas(self, bg = 'black', height = int(self.Height), width = int(self.Width))
        self.canvas.pack()
        self.canvas.place(x = 30, y = 30)
        self.canvas.bind("<Button-1>",func = self.handler_adaptor(fun = self.FramePosition, mycanvas = self.canvas))
        self.Framex = []
        self.Framey = []
        
        self.scan = Scan(self.Width//2,self.Height,30,50)
        self.scan.startPipeline()
        self.wait_frame = False
        
        
        self.ButtonPlaceBasex = 30 + 1280 + 30
        self.ButtonPlaceBasey = 60
        self.ComponentCount = 0
    
        self.capture_button = tk.Button(self, text = 'Capture', font = ('Arial', 14, "bold", "italic"), width = 16, height = 1, command = self.Capture)
        self.capture_button.pack()
        self.capture_button.place(x = self.ButtonPlaceBasex, y = self.ButtonPlaceBasey + 50*self.ComponentCount, anchor = 'nw')
        self.ComponentCount += 1
        
        
    def handler_adaptor(self,fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)
    
    
    def FramePosition(self,event, mycanvas):
        if len(self.Framex) < 2 and len(self.Framey) < 2:
            self.Framex.append(event.x)
            self.Framey.append(event.y)
            mycanvas.create_oval(event.x-2,event.y-2,event.x+2,event.y+2, fill = 'red')
        else:
            mycanvas.create_rectangle(self.Framex[0], self.Framey[0], self.Framex[1], self.Framey[1], outline = 'red', width = '4')
            self.Framex = []
            self.Framey = []
            
    def Capture(self):
        
        if self.wait_frame == False:
            self.wait_frame = True
            self.scan.waitPhoto()
        self.scan.takePhoto()
        #cv2.imwrite('color_image'+str(1)+'.jpg', scan.giveImageArray())
        self.color_image = self.scan.Image_alignment()
        self.color_image = cv2.cvtColor(self.color_image, cv2.COLOR_RGB2BGR)
        self.img_open = Image.fromarray(self.color_image)
        self.img_png = ImageTk.PhotoImage(self.img_open)
        self.canvas.create_image(self.Width//2 + 1, 1, anchor='n',image=self.img_png)
    def closeWindow(self):
        if self.scan.pipe:
            self.scan.stopPipeline()
        self.destroy()    


# In[24]:


if __name__ == "__main__":
    app = App()
    app.protocol('WM_DELETE_WINDOW', app.closeWindow)
    app.mainloop()


# In[ ]:



