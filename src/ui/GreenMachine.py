from imutils.video import VideoStream
from ui import UI
import cv2

stream = cv2.VideoCapture(0)
stream.set(3,720)
stream.set(4,360)

ui = UI(stream)
ui.master.mainloop()
