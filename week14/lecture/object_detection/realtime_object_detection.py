import cv2
import numpy as np
import time

def object_detection(image):
    image_height, image_width, _ = image.shape
    # create blob from image
    blob = cv2.dnn.blobFromImage(image=image, size=(160, 120), swapRB=True)

    model.setInput(blob)
    # forward pass through the model to carry out the detection
    output = model.forward()    
    print('output shape', output.shape)

    # loop over each of the detection
    for detection in output[0, 0, :, :]:
        # extract the confidence of the detection
        confidence = detection[2]
        # draw bounding boxes only if the detection confidence is above...
        # ... a certain threshold, else skip
        if confidence > .4:
            # get the class id
            class_id = detection[1]
            # map the class id to the class
            class_name = class_names[int(class_id)-1]
            color = COLORS[int(class_id)]
            # get the bounding box coordinates
            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            # get the bounding box width and height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height
            # draw a rectangle around each detected object
            cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
            # put the FPS text on top of the frame
            cv2.putText(image, class_name, (int(box_x), int(box_y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return image

def main():
    process_times = []
    current_fps = 30
    
    while(camera.isOpened()):
        _, image = camera.read()
        image = cv2.flip(image, -1)

        before_D = time.time()
        image = object_detection(image)
        after_D = time.time()
        
        process_time = after_D - before_D
        process_times.append(process_time)

        if len(process_times) > 10:
            process_times.pop(0)
            avg_process_time = sum(process_times) / len(process_times)
            new_fps = min(30, int(1 / avg_process_time))
            
            if new_fps != current_fps:
                current_fps = new_fps
                camera.set(cv2.CAP_PROP_FPS, current_fps)

        cv2.imshow('Detectioned Image', image)

        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    camera.set(cv2.CAP_PROP_FPS, 30)

    class_names = []
    with open('object_detection_classes_coco.txt', 'r') as f:
        class_names = f.read().split('\n')
    print(class_names)
    COLORS = np.random.uniform(0, 255, size=(len(class_names), 3))

    model = cv2.dnn.readNetFromTensorflow(model='frozen_inference_graph.pb', config='ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

    main()

    cv2.destroyAllWindows()