import numpy as np
import tensorflow as tf
from vidgear.gears import CamGear
import cv2
from threading import Thread

WIDTH = 720
HEIGHT = 480
URL = "https://www.twitch.tv/betboom_ru2"
model_path = "ssdlite_mobilenet_v2.tflite"
type_list = ["got mask", "no mask", "wear incorrectly"]
frame = None
output = None
done = False


def model_init(path: str):
    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details


def imread(img, shape):
    if img is not None:
        img_ = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_ = cv2.resize((img_ * 2 / 255) - 1, (shape, shape))
        img_ = img_[np.newaxis, :, :, :].astype("float32")
        return img_


def cam_running(cam):
    global frame
    global done
    while not done:
        frame = cam.read()


def get_output(interpreter, output_details, i_detail, cam, shape):
    global output
    global done
    while not done:
        img = cam.read()
        output_frame = imread(img, shape)
        interpreter.set_tensor(i_detail[0]["index"], output_frame)
        interpreter.invoke()
        boxes = interpreter.get_tensor(output_details[0]["index"])
        classes = interpreter.get_tensor(output_details[1]["index"])
        scores = interpreter.get_tensor(output_details[2]["index"])
        num = interpreter.get_tensor(output_details[3]["index"])
        output = [boxes, classes, scores, num]


def draw_and_show(box, classes, scores, num, frame):
    for i in range(int(num[0])):
        if scores[0][i] > 0.8:
            y, x, bottom, right = box[0][i]
            x, right = int(x * WIDTH), int(right * WIDTH)
            y, bottom = int(y * HEIGHT), int(bottom * HEIGHT)
            class_type = type_list[int(classes[0][i])]
            label_size = cv2.getTextSize(class_type, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)
            color = (0, 255, 0) if class_type == type_list[0] else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (right, bottom), color, thickness=2)
            cv2.rectangle(
                frame, (x, y - 18), (x + label_size[0][0], y), color, thickness=-1
            )
            cv2.putText(
                frame,
                class_type,
                (x, y - 5),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )
    return frame


def main():
    global frame
    global done
    stream = CamGear(source=URL,stream_mode=True).start()
    interpret, i_detail, o_detail = model_init(model_path)
    camera = Thread(target=cam_running, args=(stream,))
    inference = Thread(
        target=get_output,
        args=(interpret, o_detail, i_detail, stream, i_detail[0]["shape"][1]),
    )
    camera.start()
    inference.start()
    # logging.info(msg="Start inference")
    while not done:
        if frame is None:
            break
        if output == None:
            pass
        else:
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            frames = draw_and_show(*output, frame)
            cv2.imshow("Mask detect", frames)
        key = cv2.waitKey(10)
        if key == 27:
            done = True
            camera.join()
            inference.join()
            cv2.destroyAllWindows()
            stream.stop()
            exit()


if __name__ == "__main__":
    main()
