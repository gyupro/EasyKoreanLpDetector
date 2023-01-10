# EasyKoreanLpDetector

[테스트 URL](http://aifolio.cafe24.com/LP/)
깃헙에 어렵고 잘 안 돼는 한국 번호판 인식기밖에 없어서 공개합니다.
도움이 되셨다면 스타한개 부탁드려요!

알고리즘

이미지가 입력으로 들어오면 자동차 인식 -> 자동차 내부에서 번호판 인식 -> 번호판에서 글자 인식입니다.

자동차, 번호판 인식(https://github.com/ultralytics/yolov5)  
번호판 글자 인식(https://github.com/JaidedAI/EasyOCR)  
데이터셋 (https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=172)  

|잘 되는 예시|잘 안되는 예시|설명|
|------|---|---|
|테스트1|테스트2|테스트3|
|테스트1|테스트2|테스트3|
|테스트1|테스트2|테스트3|

강점 :
1. 깃헙의 타 프로젝트들보다 인식을 잘합니다.
2. 코드가 쉽습니다.
3. GPU가 있으시면 비교적 빠릅니다. (0.1초?)
4. 추가 학습을 통해 성능이 올라갈수 있습니다. (학습방법 위의 오픈소스 참고)

한계 :
1. 학습을 완벽하게 시키진 않았습니다. 자동차 학습도 yolov5 기본 모델로 됐기때문에, 차가 가까우면 차 자체를 인식을 하지 못합니다.
2. 번호판도 다양하게 학습시키지 않아서, 예전 번호판 등은 안되는것도 있습니다. 요즘건 비교적 잘됩니다.
