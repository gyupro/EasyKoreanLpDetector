# EasyKoreanLpDetector

Korean | [English](README.md) 


[테스트 URL](http://aifolio.cafe24.com/LP/)  
깃헙에 어렵고 잘 안 돼는 한국 번호판 인식기밖에 없어서 공개합니다.
도움이 되셨다면 스타한개 부탁드려요!

알고리즘

이미지가 입력으로 들어오면 자동차 인식 -> 자동차 내부에서 번호판 인식 -> 번호판에서 글자 인식입니다.

자동차, 번호판 인식(https://github.com/ultralytics/yolov5)  
번호판 글자 인식(https://github.com/JaidedAI/EasyOCR)  
데이터셋 (https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=172)  

requirements  
yolov5, streamlit, easyocr, pytorch, opencv, numpy.

pip으로 모두 다운 가능하니, 라이브러리 관련 에러가나면 pip으로 다운로드 부탁드립니다.

모든 weight들이 github 프로젝트에 올라가있기때문에 50MB정도 됍니다. (따로 다운로드 받으실것 없습니다.)

git clone https://github.com/gyupro/EasyKoreanLpDetector/ 로 프로젝트를 다운받으신 후,
streamlit run server.py 로 streamlit 서버를 실행시키세요.

```bash
git clone https://github.com/gyupro/EasyKoreanLpDetector/
cd EasyKoreanLpDetector
streamlit run server.py
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
1. 학습을 완벽하게 시키진 않았습니다. 자동차 검출도 yolov5 기본 모델로 했기때문에, 차가 가까우면 차 자체를 인식을 하지 못합니다.
2. 번호판도 다양하게 학습시키지 않아서, 예전 번호판 등은 안되는것도 있습니다. 요즘건 비교적 잘됩니다.

### 학습:
* AIHUB 데이터를 활용했습니다. [AIHUB dataset](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=172)
* OCR은 번호판, 캐릭터 데이터셋 80,000장 정도 이용했습니다.
* AIHUB의 데이터셋은 번호판이 차에서 블러가 돼있기 때문에, 크롭된 번호판을 블러된 위치에 붙여서 검출학습 시켰습니다.
