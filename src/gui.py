from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tk
from Tkinter import N, S, E, W
import threading
import datetime
import imutils
import cv2
import os
import numpy as np

class UI:
    def __init__(self, stream, model):
        self.stream = stream
        self.model = model

        self.master = tk.Tk()
        self.master.configure(background='black')
        self.master.attributes("-fullscreen", True)

        defaultImg = ImageTk.PhotoImage(file="default.gif")
        self.panel = tk.Label(image=defaultImg)
        self.panel.image = defaultImg
        self.panel.grid(row=1, column=0)
	
        close_button = tk.Button(self.master, text="X", command=self.kill, width=2, bg="pink", font=("Ubuntu", 28), borderwidth=0)
        close_button.grid(row=0, column=0, sticky=N+E)

        self.alive = True
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.master.wm_title("DGM GreenMachine")
        
    def videoLoop(self):
        try:
            while self.alive:
                _, self.frame = self.stream.read()

                image_resized = cv2.resize(self.frame, (960, 720))

                output = self.model.predict(image_resized[None, ...])

                boxes = output['boxes'][0]
                scores = output['scores'][0]
                classes = output['classes'][0]
                score_thresh = 0.1

                for i in range(len(scores)):
                    #print(scores[i])
                    if scores[i] > score_thresh:
                        box = boxes[i] * np.array([self.frame.shape[0], self.frame.shape[1], self.frame.shape[0], self.frame.shape[1]])
                        cv2.rectangle(self.frame, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (0,255,0), 3)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(self.frame, str(classes[i] + 1), (int(box[1]), int(box[0]) - 20), font, 1.0,(0,255,0), lineType=cv2.LINE_AA)

                image = Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
                image = ImageTk.PhotoImage(image)

                self.panel.configure(image=image)
                self.panel.image = image

        except RuntimeError, e:
            print(e)
		
    def kill(self):
        self.alive = False
        self.master.quit()
		
    def onClose(self):
        self.alive = False
        self.master.quit()
