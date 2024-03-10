from PIL import Image
import numpy as np
import cv2

classes_names = ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
                 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
                 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
                 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse',
                 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
                 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
model = cv2.dnn.readNet(r"C:\Users\Lenovo\PycharmProjects\camapp\yolo\yolov3.cfg",r"C:\Users\Lenovo\PycharmProjects\camapp\yolo\yolov3.weights")
layer_names = model.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in model.getUnconnectedOutLayers()]
output_layers = [layer_names[i-1] for i in model.getUnconnectedOutLayers()]
# output_layers = [layer_names[i-1] for i in model.getUnconnectedOutLayers()]


def check(path):

    image = Image.open(path)
    div = image.size[0] / 500
    resized_image = image.resize((round(image.size[0] / div), round(image.size[1] / div)))
    resized_image.save('na.jpg')
    image = cv2.imread("na.jpg")
    height, width, channels = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    model.setInput(blob)
    outputs = model.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for output in outputs:
        for identi in output:
            scores = identi[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.8:
                class_ids.append(class_id)

    if 63 in class_ids and 67 in class_ids:
        print('cell phone and laptop nearby')




        return "cell phone and laptop nearby"
    elif 67 in class_ids:
        print('cell phone found')
        return "cell phone found"
    elif 63 in class_ids:
        print('laptop found')
        return "laptop found"
    else:
        return "no"
