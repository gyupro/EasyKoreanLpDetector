# EasyKoreanLpDetector

Korean | [English](README.md) 


[테스트 URL](http://aifolio.cafe24.com/LP/)  
깃헙에 어렵고 잘 안 돼는 한국 번호판 인식기밖에 없어서 공개합니다.
도움이 되셨다면 스타한개 부탁드려요!

알고리즘

이미지가 입력으로 들어오면 자동차 인식(YOLO26s) -> 자동차 내부에서 번호판 인식(YOLOv5) -> 번호판에서 글자 인식입니다.

> 자동차 검출기는 **Ultralytics YOLO26s**로 업그레이드되었습니다 (NMS-free, CPU 추론 속도 향상). 번호판 검출기는 기존 YOLOv5 학습 가중치(`lp_det.pt`)를 그대로 사용합니다.

자동차 인식(https://github.com/ultralytics/ultralytics) — YOLO26  
번호판 인식(https://github.com/ultralytics/yolov5)  
번호판 글자 인식(https://github.com/JaidedAI/EasyOCR)  
데이터셋 (https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=172)  

## Requirements

번호판 검출 weight는 프로젝트에 포함되어 있습니다 (약 50MB). 자동차 검출 weight (`yolo26s.pt`, 약 20MB)는 첫 실행 시 Ultralytics가 자동으로 다운로드합니다.

**pip**
```bash
pip install -r requirements.txt
```

**uv (권장)**
```bash
uv venv --python 3.11
uv pip install -r requirements-uv.txt --index-url https://download.pytorch.org/whl/cpu
```

## 실행 방법

```bash
git clone https://github.com/gyupro/EasyKoreanLpDetector/
cd EasyKoreanLpDetector
streamlit run server.py --server.headless true
```

 
|잘 되는 예시|잘 되는 예시|잘 안되는 예시|
|----|----|----|
|![예시](detected/결과.PNG)|![예시](detected/캡처.PNG)|![예시](undetected/캡처.PNG)|  
|![image](https://user-images.githubusercontent.com/79894531/211469966-db8fa936-1814-4424-b8cc-f0502f361995.png)|![image](https://user-images.githubusercontent.com/79894531/211470161-27ba5b81-8453-4edf-b485-92ae35524d0f.png)||


강점 :
1. 깃헙의 타 프로젝트들보다 인식을 잘합니다.
2. 코드가 쉽습니다.
3. GPU가 있으시면 비교적 빠릅니다. (0.1초?)
4. 추가 학습을 통해 성능이 올라갈수 있습니다. (학습방법 위의 오픈소스 참고)
5. 휴대폰으로 찍은 4K 사진들이 잘됩니다.

한계 :
1. 자동차 검출은 COCO 사전학습 YOLO26s 모델을 사용합니다. 차가 화면을 거의 채울 정도로 가까우면 검출이 안 될 수 있고, 그 경우엔 번호판 검출기가 전체 이미지에서 직접 동작하도록 fallback 처리가 되어 있습니다.
2. 번호판도 다양하게 학습시키지 않아서, 예전 번호판 등은 안되는것도 있습니다. 요즘건 비교적 잘됩니다.

### 학습:
* AIHUB 데이터를 활용했습니다. [AIHUB dataset](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=172)
* OCR은 번호판, 캐릭터 데이터셋 80,000장 정도 이용했습니다.
* AIHUB의 데이터셋은 번호판이 차에서 블러가 돼있기 때문에, 크롭된 번호판을 블러된 위치에 붙여서 검출학습 시켰습니다.
