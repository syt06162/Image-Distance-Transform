# Distance-Transform
distance transform : D4 (city block), D8 (chessboard), DE (Euclidean) "without" OpenCV2
OpenCV2 함수를 사용하지 않고, distance transform 직접 구현.

## 이론
![image](https://user-images.githubusercontent.com/92567571/227986435-97d00f63-df03-4f3d-8016-8e83f4a65e0a.png)
imgsrc :: Sonka, Milan, Vaclav Hlavac, and Roger Boyle. Image processing, analysis, and machine vision. 4th ed. Cengage Learning, 2014.
binary 이미지에서 각 픽셀들의 object와의 "거리"를 나타낸다.
"거리"에 대한 정의는 아래와 같이 크게 3가지가 있다.
![image](https://user-images.githubusercontent.com/92567571/227986088-42d73256-7e63-47f8-bcfd-7b5bf2711912.png)

## 기능
binary 이미지 파일 이름을 input으로 넣으면, src - D4 - D8 - DU 의 결과를 모두 합친 한 개의 이미지를 output으로 저장한다..
![image](https://user-images.githubusercontent.com/92567571/227989783-7b87cb38-95f5-4a0a-b45a-12a68f950fce.png)


## 구현 원리
- python 3
- OpenCV2 라이브러리로는 쉽게 구현할 수 있는 기능이지만, 해당 함수를 사용하지 않고 직접 코드로 구현하였다. 
- DE (Euclidean)의 경우에는 작은 이미지에 대해서는 필자의 구현 방법으로 잘 작동한다. 
그러나 image size가 매우 큰 경우에는 시간이 매우 오래걸려 추천하지 않는다.
따라서, 이의 경우는 OpenCV2의 라이브러리의 함수를 이용한다.
distance_transform.py 코드의 2번째줄의 DE_LABEL=1 이면 OpenCV2 라이브러리를 이용, DE_LABEL=2이면 필자의 코드를 이용한다.
기본값은 DE_LABEL=1 이다.
- D4, D8의 구현 방법은 아래 공식을 따른다.
![image](https://user-images.githubusercontent.com/92567571/227988417-6035dea9-1969-4d66-b4c5-71d9ff9676bc.png)
- DE의 경우 필자는 BFS 알고리즘을 응용하여 작성하였다. 이는 직접 최단 거리를 찾는 방법으로, 시간 복잡도가 크다.

## 사용 방법
- distance_transform.py 파일과 같은 경로에 image 파일을 둔다.
- 코드의 1번째 줄에 OPEN_IMAGE_NAME 변수에 해당 image 파일의 파일 이름을 확장자까지 포함해서 작성한다.
- 코드를 실행하면 이미지 결과 창이 띄워지며, 결과 이미지가 같은 경로에 저장된다.
