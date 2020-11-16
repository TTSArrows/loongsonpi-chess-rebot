import os
import shutil


names = os.listdir('img')
for name in names:
    img_path = os.path.join('img', name)
    cmd = './darknet detector test cheese.data yolov3-tiny-cheese-test.cfg yolov3-tiny-cheese-train_14000.weights ' + img_path
    os.system(cmd)
    src = 'predictions.jpg'
    dst = os.path.join('img_results', name.split('.')[0] + '_prediction.jpg')
    shutil.copy(src, dst)
    print('copy:', src, ' to:', dst)



