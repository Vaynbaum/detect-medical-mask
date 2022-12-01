import random
from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
import numpy as np
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential, load_model
from keras.utils import image_utils
import cv2
from keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
from neural_network.const import TITLE, TYPE_LIST
import numpy as np
from skimage.transform import resize_local_mean
from PIL import Image as im

WIDTH = 720
HEIGHT = 480
NAME_MODEL = "models/mymodel.h5"
NAME_FILE = "models/haarcascade_frontalface_default.xml"
PATH_ASSETS = "../../assets/dataset"
PATH_TEMP = "temp.jpg"


def train_save_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(150, 150, 3)))
    model.add(MaxPooling2D())
    model.add(Conv2D(32, (3, 3), activation="relu"))
    model.add(MaxPooling2D())
    model.add(Conv2D(32, (3, 3), activation="relu"))
    model.add(MaxPooling2D())
    model.add(Flatten())
    model.add(Dense(100, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True
    )
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    training_set = train_datagen.flow_from_directory(
        f"{PATH_ASSETS}/train",
        target_size=(150, 150),
        batch_size=16,
        class_mode="binary",
    )
    test_set = test_datagen.flow_from_directory(
        f"{PATH_ASSETS}/test",
        target_size=(150, 150),
        batch_size=16,
        class_mode="binary",
    )

    model_saved = model.fit_generator(
        training_set,
        epochs=10,
        validation_data=test_set,
    )
    model.save(NAME_MODEL, model_saved)


def detect_by_iamge():
    mymodel = load_model(NAME_MODEL)
    test_image = image_utils.load_img(PATH_TEMP, target_size=(150, 150, 3))
    test_image = image_utils.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    mymodel.predict(test_image)[0][0]


# IMPLEMENTING LIVE DETECTION OF FACE MASK
def init_model(path: str):
    mymodel = load_model(NAME_MODEL)
    cap = cv2.VideoCapture(path)
    face_cascade = cv2.CascadeClassifier(NAME_FILE)
    return mymodel, cap, face_cascade


def save_video(path: str, out_path: str):

    mymodel, cap, face_cascade = init_model(path)
    width = int(cap.get(CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(CAP_PROP_FPS))

    codec = "mp4v" if Path(out_path).suffix == ".mp4" else "MJPG"
    out = cv2.VideoWriter(
        out_path, cv2.VideoWriter_fourcc(*f"{codec}"), fps, (width, height)
    )
    while cap.isOpened():
        _, img = cap.read()
        if img is None:
            break
        img = detect_by_video(mymodel, face_cascade, img, width=width, height=height)
        if img is not None:
            out.write(img)
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def watch_video(path: str):
    statistics = list()
    mymodel, cap, face_cascade = init_model(path)
    i = 0
    while cap.isOpened():
        _, img = cap.read()
        if img is None:
            break
        if i == 0:
            obj = {}
            img = detect_by_video(mymodel, face_cascade, img, obj)
            statistics.append(obj)
            if img is not None:
                cv2.imshow(TITLE, img)
            if cv2.waitKey(10) == 27:
                break
            if cv2.getWindowProperty(TITLE, cv2.WND_PROP_VISIBLE) < 1:
                break
        i += 1
        i %= 5
    cap.release()
    cv2.destroyAllWindows()
    return statistics


def draw_text(
    img,
    text,
    font=cv2.FONT_HERSHEY_PLAIN,
    pos=(0, 0),
    font_scale=3,
    font_thickness=2,
    text_color=(0, 255, 0),
    text_color_bg=(0, 0, 0),
):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (20 + x + text_w, 20 + y + text_h), text_color_bg, -1)
    cv2.putText(
        img,
        text,
        (10 + x, 10 + y + text_h + font_scale - 1),
        font,
        font_scale,
        text_color,
        font_thickness,
    )


def blue(img):
    arr = np.copy(img)
    for x in arr:
        for y in x:
            if not (y[0] > 220 and y[1] > 220 and y[2] > 220):
                y[0] = int(y[0] * 0.5870)
                y[1] = int(y[1] * 0.1140)
                y[2] = int(y[2] * 0.2989)
    return arr


def detect_by_video(mymodel, face_cascade, img, obj=None, width=WIDTH, height=HEIGHT):
    img = cv2.resize(img, (width, height))
    face = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4)
    cnt_without = 0
    is_obj = obj is not None
    if is_obj:
        obj["objects"] = []
        objects = []
    i = 0
    for (x, y, w, h) in face:
        if i == 0:
            face_img = img[y : y + h, x : x + w]
            cv2.imwrite(PATH_TEMP, face_img)
            test_image = image_utils.load_img(PATH_TEMP, target_size=(150, 150, 3))
            test_image = image_utils.img_to_array(test_image)

            # face_img = im.fromarray(face_img)
            # face_img = blue(face_img)
            # test_image = image_utils.img_to_array(face_img)
            # test_image = resize_local_mean(test_image, (150, 150, 3))
            # cv2.imwrite(PATH_TEMP, test_image)

            test_image = np.expand_dims(test_image, axis=0)
            pred = mymodel.predict(test_image)[0][0]
            text = TYPE_LIST[1] if pred == 1 else TYPE_LIST[0]
            color = (0, 0, 255) if pred == 1 else (0, 255, 0)
            cnt_without += 1 if pred == 1 else 0
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                img,
                text,
                (x, y + h + 20 * int(width // WIDTH)),
                cv2.FONT_HERSHEY_SIMPLEX,
                int(width // WIDTH),
                color,
                int(width // WIDTH),
                cv2.LINE_AA,
            )
            if is_obj:
                objects.append(
                    {
                        "class": int(pred),
                        "coord": {
                            "x": int(x),
                            "y": int(y),
                            "width": int(w),
                            "height": int(h),
                        },
                        "probability": random.randrange(0, 100),
                    }
                )
        i += 1
        i %= 3
    try:
        cnt_all = face.size / 4
        if is_obj:
            obj["count"] = int(cnt_all)
            obj["objects"] = objects
        res = int(cnt_without / (cnt_all) * 100)
        draw_text(
            img,
            f"No mask: {res}%",
            cv2.FONT_HERSHEY_SIMPLEX,
            (0, 0),
            int(width // WIDTH),
            int(width // WIDTH),
            (255, 0, 0),
            (255, 255, 255),
        )
        return img
    except:
        pass
    return None
