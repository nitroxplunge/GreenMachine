from imutils.video import VideoStream
from gui import UI
import cv2
import tensorflow.contrib.tensorrt as trt
import tensorflow as tf
import numpy as np
from jetnet.tensorflow import TFModel, download_detection_model, build_detection_graph

DATA_DIR = './models/dgm-cafeteria-objects/'

config_path = DATA_DIR + 'model.config'
checkpoint_path = DATA_DIR + 'model.ckpt'
graph_path = DATA_DIR + 'graph.pbtxt'

frozen_graph, input_names, output_names = build_detection_graph(
    config=config_path,
    checkpoint=checkpoint_path
)

print output_names

trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)

with open(graph_path, 'wb') as f:
    f.write(trt_graph.SerializeToString())

model = TFModel(trt_graph, output_names)

stream = cv2.VideoCapture(1)
stream.set(3,960)
stream.set(4,720)

ui = UI(stream, model)
ui.master.mainloop()
