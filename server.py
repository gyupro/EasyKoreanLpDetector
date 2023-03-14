import streamlit as st
import requests
import json
from glob import glob
import torch
import easyocr
import numpy as np
import cv2

from PIL import ImageFont, ImageDraw, Image
st.set_page_config(layout='wide')

def main():
    car_m, lp_m, reader = load_model()
    st.title("자동차 번호판 인식")
    file = st.file_uploader('이미지를 올려주세요')
    if file:
        im, text = detect(car_m, lp_m, reader, file)
        st.write(text)
        st.image(im)
        
@st.cache
def load_model():
    car_m = torch.hub.load("ultralytics/yolov5", 'yolov5s', force_reload=True, skip_validation=True)
    lp_m = torch.hub.load('ultralytics/yolov5', 'custom', 'lp_det.pt')
    reader = easyocr.Reader(['en'], detect_network='craft', recog_network='best_acc', user_network_directory='lp_models/user_network', model_storage_directory='lp_models/models')

    car_m.classes = [2,3, 5, 7]
    return car_m, lp_m, reader

import os

def detect(car_m, lp_m, reader, path):
    fontpath = "SpoqaHanSansNeo-Light.ttf"
    font = ImageFont.truetype(fontpath, 200)
    im = Image.open(path)

    im.save(path)
    to_draw = np.array(im)
    results = car_m(im)
    locs = results.xyxy[0]
    
        
    result_text = []

    if len(locs) == 0:
        
        result = lp_m(im)
        if len(result) == 0:
            result_text.append('검출된 차 없음')
        else:
            for rslt in result.xyxy[0]:
                x2,y2,x3,y3 = [item1.cpu().detach().numpy().astype(np.int32) for item1 in rslt[:4]]
                try:
                    extra_boxes = 0
                    im = cv2.cvtColor(cv2.resize(to_draw[y2 - extra_boxes:y3 + extra_boxes,x2 - extra_boxes:x3 + extra_boxes], (224,128)), cv2.COLOR_BGR2GRAY)
                    text = reader.recognize(im)[0][1]
                    result_text.append(text)
                except Exception as e:
                    return cv2.resize(to_draw, (1280,1280)), ""
                img_pil = Image.fromarray(to_draw)
                draw = ImageDraw.Draw(img_pil)
                draw.text( (x2-100,y2-300),  text, font=font, fill=(255,0,255))
                to_draw = np.array(img_pil)
                st.write((x2.item(),y2))
                cv2.rectangle(to_draw, (x2.item(),y2.item()),(x3.item(),y3.item()),(255,0,255),10)

            return cv2.resize(to_draw, (1280,1280)), result_text
    
    for idx, item in enumerate(locs):
        x,y,x1,y1=[it.cpu().detach().numpy().astype(np.int32) for it in item[:4]]
        car_im = to_draw[y:y1, x:x1,:].copy()
        result = lp_m(Image.fromarray(car_im))
        
        if len(result) == 0:
            result_text.append("차는 검출됬으나, 번호판이 검출되지 않음")
        
        for rslt in result.xyxy[0]:
            x2,y2,x3,y3 = [item1.cpu().detach().numpy().astype(np.int32) for item1 in rslt[:4]]
            try:
                extra_boxes = 0
                im = cv2.cvtColor(cv2.resize(to_draw[y+y2 - extra_boxes:y+y3 + extra_boxes,x+x2 - extra_boxes:x+x3 + extra_boxes], (224,128)), cv2.COLOR_BGR2GRAY)
                text = reader.recognize(im)[0][1]
                result_text.append(text)
            except Exception as e:
                return cv2.resize(to_draw, (1280,1280)), ""
            img_pil = Image.fromarray(to_draw)
            draw = ImageDraw.Draw(img_pil)
            draw.text( (x+x2-100,y+y2-300),  text, font=font, fill=(255,0,255))
            to_draw = np.array(img_pil)
            cv2.rectangle(to_draw, (x+x2,y+y2),(x+x3,y+y3),(255,0,255),10)
    
    return cv2.resize(to_draw, (1280,1280)), result_text
        
if __name__ == '__main__':

    main()
