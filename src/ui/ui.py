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

class UI:
	def __init__(self, stream):
		self.stream = stream

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
				self.frame = imutils.resize(self.frame, width=1280)

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

