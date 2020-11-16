import os


os.system('./darknet detector test cfg/voc.data cfg/yolov3-tiny.cfg models/1/yolov3-tiny_900.weights VOCdevkit/VOC2007/JPEGImages/left0.jpg')
print('Done')
