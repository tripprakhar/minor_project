# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 22:59:49 2021

@author: hp
"""

import tkinter as tk
import cv2
import os
import operator
from PIL import Image, ImageTk
from keras.models import model_from_json
from keras.preprocessing import image
from string import ascii_uppercase
import numpy as np

path=os.getcwd()
class GUI:
    def __init__(self):
        self.cap=cv2.VideoCapture(0)
        self.video_panel_image= None
        self.filter_panel_image= None
        self.directory='model'
        
        self.json_file = open(self.directory+"/model-bw.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(self.directory+"/model-bw.h5")
        
        self.json_file_dru = open(self.directory+"/model-bw-dru.json" , "r")
        self.model_json_dru = self.json_file_dru.read()
        self.json_file_dru.close()
        self.loaded_model_dru = model_from_json(self.model_json_dru)
        self.loaded_model_dru.load_weights(self.directory+"/model-bw-dru.h5")

        self.json_file_tkdi = open(self.directory+"/model-bw-tkdi.json" , "r")
        self.model_json_tkdi = self.json_file_tkdi.read()
        self.json_file_tkdi.close()
        self.loaded_model_tkdi = model_from_json(self.model_json_tkdi)
        self.loaded_model_tkdi.load_weights(self.directory+"/model-bw-tkdi.h5")

        self.json_file_smn = open(self.directory+"/model-bw-mns.json" , "r")
        self.model_json_smn = self.json_file_smn.read()
        self.json_file_smn.close()
        self.loaded_model_smn = model_from_json(self.model_json_smn)
        self.loaded_model_smn.load_weights(self.directory+"/model-bw-mns.h5")
        
        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        for i in ascii_uppercase:
          self.ct[i] = 0
        
        self.root=tk.Tk()
        self.root.title("Sign to Text Converter")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("900x1100+0+0")
        
        #Heading
        self.heading = tk.Label(self.root,text = "ASL recognition using CNN",font=("Comic Sans MS",23,"bold"))
        self.heading.place(x=180,y = 5)
        
        #Video Panel For Camera Input
        self.video=tk.Label(self.root)
        self.video.place(x = 135, y = 10, width = 640, height = 640)
        
        #Filtered image Panel
        self.filter =tk.Label(self.root)
        self.filter.place(x = 460, y = 95, width = 310, height = 310)
        
        #Character Panel
        self.charpanel =tk.Label(self.root) # Current SYmbol
        self.charpanel.place(x = 500,y=640)
        #Character text
        self.char =tk.Label(self.root)
        self.char.place(x = 10,y = 640)
        self.char.config(text="Character :",font=("Courier",30,"bold"))
        
        #Word Panel
        self.wordpanel =tk.Label(self.root) 
        self.wordpanel.place(x = 220,y=700)
        #Word text
        self.word =tk.Label(self.root)
        self.word.place(x = 10,y = 700)
        self.word.config(text ="Word :",font=("Courier",30,"bold"))
        
        #Sentence Panel
        self.senpanel =tk.Label(self.root)
        self.senpanel.place(x = 350,y=760)
        self.sent =tk.Label(self.root)
        self.sent.place(x = 10,y = 760)
        self.sent.config(text ="Sentence :",font=("Courier",30,"bold"))
        
        self.current_symbol=None
        self.str=""
        self.word=""
        self.video_loop()
        
        
    def destructor(self):
        print("Closing Application...")
        self.root.destroy() #Destroying Main Window
        self.cap.release() #Releasing Camera
        cv2.destroyAllWindows()
        
   
        
    def video_loop(self):
        ret, frame = self.cap.read()
        if ret:
             img = cv2.flip(frame, 1)
            #Flipping 2-D array
            #flipcode = 0, About x-axis
            #flipcode = 1, about y-axis
            #flipcode = -1, about both
            
             x1 = int(0.5*frame.shape[1])
             y1 = 10
             x2 = frame.shape[1]-10
             y2 = int(0.5*frame.shape[1])
             cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
             
             img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
             
             self.video_panel_image=Image.fromarray(img)
             imgtk = ImageTk.PhotoImage(image=self.video_panel_image)
            
            #Configuring Video Panel defined in __init__.
             self.video.imgtk = imgtk
             self.video.config(image=imgtk)
             
             img = img[y1:y2, x1:x2]
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             blur = cv2.GaussianBlur(gray,(5,5),2)
             # https://www.geeksforgeeks.org/python-thresholding-techniques-using-opencv-set-2-adaptive-thresholding/
             th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
            
            # https://www.geeksforgeeks.org/python-thresholding-techniques-using-opencv-set-1-simple-thresholding/r
            #First argument is the source image, which should be a grayscale image.
             retval, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            # m,n=res.shape
            # img_new=np.zeros([m,n])
             #for i in range(1, m-1):
              #   for j in range(1, n-1):
               #      temp = [res[i-1, j-1], 
                #             res[i-1, j], 
                #              res[i-1, j + 1], 
                 #             res[i, j-1], 
                  #            res[i, j], 
                   #          res[i + 1, j-1], 
                     #         res[i + 1, j], 
                   #           res[i + 1, j + 1]]
                   #  temp = sorted(temp) 
                    # img_new[i, j]= temp[4] 
            
            
            
             #img_new=img_new.astype(np.uint8)
             #res=img
             self.predict(res)
            #retval is used in Otsu thresholding  image binarization -- https://medium.com/@hbyacademic/otsu-thresholding-4337710dc519
             '''For this, our cv2.threshold() function is used, but pass an extra flag, cv2.THRESH_OTSU. For threshold value, simply
                pass zero. Then the algorithm finds the optimal threshold value and returns you as the second output, retVal.
                If Otsu thresholding is not used, retVal is same as the threshold value you used.'''
            #res is our thresholded image
             self.filter_panel_image=Image.fromarray(res)
             imgtk=ImageTk.PhotoImage(image=self.filter_panel_image)
             
             #configuring filter panel defined in __init__
             self.filter.imgtk=imgtk
             self.filter.config(image=imgtk)
             self.charpanel.config(text=self.current_symbol,font=("Courier",20))
             self.wordpanel.config(text=self.word,font=("Courier",20))
             self.senpanel.config(text=self.str,font=("Courier",20))
             
            
            
            
             
        self.root.after(5, self.video_loop)
          
            
    def predict(self,test_image):
        test_image = cv2.resize(test_image, (128,128))
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))
        result_dru = self.loaded_model_dru.predict(test_image.reshape(1 , 128 , 128 , 1))
        result_tkdi = self.loaded_model_tkdi.predict(test_image.reshape(1 , 128 , 128 , 1))
        result_smn = self.loaded_model_smn.predict(test_image.reshape(1 , 128 , 128 , 1))
        prediction={}
        prediction['blank'] = result[0][0]
        inde = 1
        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1
        #LAYER 1
        new_dict=dict([(value,key) for key,value in prediction.items()])
        prediction = sorted(prediction.items(),key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]
        print(self.current_symbol)
        #Layer 2
       
        if(self.current_symbol == 'blank'):
            for i in ascii_uppercase:
                self.ct[i] = 0
                
        self.ct[self.current_symbol]+=1
        if(self.ct[self.current_symbol]>40):
            for i in ascii_uppercase:
                if(i==self.current_symbol):
                    continue
                tmp=self.ct[self.current_symbol]-self.ct[i]
                if tmp<0:
                    tmp*=-1
                if tmp<=10:
                    self.ct['blank']=0
                    for i in ascii_uppercase:
                        self.ct[i]=0
                    return
                self.ct['blank'] = 0
                for i in ascii_uppercase:
                    self.ct[i] = 0
                if self.current_symbol == 'blank':
                    if self.blank_flag == 0:
                        self.blank_flag = 1
                        if len(self.str) > 0:
                            self.str += " "
                    self.str += self.word
                    self.word = ""
                else:
                    if(len(self.str) > 16):
                        self.str = ""
                    self.blank_flag = 0
                    self.word += self.current_symbol
                
                
        
            
        
            
        
        print(prediction)
        
        
        
       
        
        
            
        
        
        
        
pba = GUI()
pba.root.mainloop()
        