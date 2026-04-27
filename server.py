import cv2
import easyocr
import numpy as np
import streamlit as st
import torch
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

FONT_PATH = "SpoqaHanSansNeo-Light.ttf"
FONT_SIZE = 200
OUTPUT_SIZE = (1280, 1280)
PLATE_SIZE = (224, 128)
COLOR = (255, 0, 255)
CAR_CLASSES = [2, 3, 5, 7]

st.set_page_config(layout="wide")


@st.cache_resource
def load_model():
    car_m = YOLO("yolo26s.pt")
    lp_m = torch.hub.load("ultralytics/yolov5", "custom", "lp_det.pt", trust_repo=True)
    reader = easyocr.Reader(
        ["en"],
        detect_network="craft",
        recog_network="best_acc",
        user_network_directory="lp_models/user_network",
        model_storage_directory="lp_models/models",
    )
    return car_m, lp_m, reader


def _xyxy(tensor):
    return [int(v.cpu().detach().numpy()) for v in tensor[:4]]


def _draw_plate(to_draw, font, ax, ay, bx, by, text):
    img_pil = Image.fromarray(to_draw)
    ImageDraw.Draw(img_pil).text((ax - 100, ay - 300), text, font=font, fill=COLOR)
    to_draw = np.array(img_pil)
    cv2.rectangle(to_draw, (ax, ay), (bx, by), COLOR, 10)
    return to_draw


def _process_plate(to_draw, reader, font, x_off, y_off, rslt, result_text):
    x2, y2, x3, y3 = _xyxy(rslt)
    ax, ay, bx, by = x_off + x2, y_off + y2, x_off + x3, y_off + y3
    try:
        gray = cv2.cvtColor(cv2.resize(to_draw[ay:by, ax:bx], PLATE_SIZE), cv2.COLOR_BGR2GRAY)
        text = reader.recognize(gray)[0][1]
    except Exception as e:
        st.warning(f"번호판 인식 실패: {e}")
        return to_draw
    result_text.append(text)
    st.write((ax, ay))
    return _draw_plate(to_draw, font, ax, ay, bx, by, text)


def detect(car_m, lp_m, reader, path):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    im = Image.open(path)
    to_draw = np.array(im)
    locs = car_m(im, classes=CAR_CLASSES, verbose=False)[0].boxes.xyxy
    result_text = []

    if len(locs) == 0:
        plates = lp_m(im).xyxy[0]
        if len(plates) == 0:
            result_text.append("검출된 차 없음")
        else:
            for rslt in plates:
                to_draw = _process_plate(to_draw, reader, font, 0, 0, rslt, result_text)
        return cv2.resize(to_draw, OUTPUT_SIZE), result_text

    for item in locs:
        x, y, x1, y1 = _xyxy(item)
        plates = lp_m(Image.fromarray(to_draw[y:y1, x:x1].copy())).xyxy[0]
        if len(plates) == 0:
            result_text.append("차는 검출됬으나, 번호판이 검출되지 않음")
        for rslt in plates:
            to_draw = _process_plate(to_draw, reader, font, x, y, rslt, result_text)

    return cv2.resize(to_draw, OUTPUT_SIZE), result_text


def main():
    car_m, lp_m, reader = load_model()
    st.title("자동차 번호판 인식")
    file = st.file_uploader("이미지를 올려주세요")
    if file:
        im, text = detect(car_m, lp_m, reader, file)
        st.write(text)
        st.image(im)


if __name__ == "__main__":
    main()
