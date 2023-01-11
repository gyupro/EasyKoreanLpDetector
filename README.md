# EasyKoreanLpDetector

English | [Korean](README-KOR.md)


[Test URL](http://aifolio.cafe24.com/LP/)  
I release this repo because there is no other options that work great on korean license plate!
Please give it a star if this is helpful

## Algorithm

Input Image -> Detect cars -> Detece license plate in a car -> OCR

## requirements  
yolov5, streamlit, easyocr, pytorch, opencv, numpy.

You can download all libraries with pip, if error occurs, download with pip

All weights are uploaded to the project, so that size of repo is about 50MB ( You don't need to download any extra )


## Steps to run

1. Download repo with git clone https://github.com/gyupro/EasyKoreanLpDetector/  
2. run streamlit server with streamlit run server.py 

```bash
git clone https://github.com/gyupro/EasyKoreanLpDetector/
cd EasyKoreanLpDetector
streamlit run server.py
```

 
|Good examples|Good examples|Bad example|
|----|----|----|
|![예시](detected/결과.PNG)|![예시](detected/캡처.PNG)|![예시](undetected/캡처.PNG)|  
|![image](https://user-images.githubusercontent.com/79894531/211469966-db8fa936-1814-4424-b8cc-f0502f361995.png)|![image](https://user-images.githubusercontent.com/79894531/211470161-27ba5b81-8453-4edf-b485-92ae35524d0f.png)||


### Advantages :
* This works better than other opensource proejcts on github
* Easiest code on github
* It's fast when you have GPU
* You can upgrade the performance by training
* It works well with 4k images that are taken from a phone

### limits :
* The train is not perfectly done, Original yolov5 model is used to detect a car so that it does not perform well when a car is close to the camera
* Old plates are sometimes not recognizable, but compared to old ones, new onews are recognized well.

## References

* [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5)

* [https://github.com/JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR)
