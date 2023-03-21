OPEN_IMAGE_NAME = "small.png"
DE_LABEL = 1

import cv2
import numpy
from collections import deque

WHITE = 255

# 사진 가져오기
src_img_original = cv2.imread(OPEN_IMAGE_NAME, cv2.IMREAD_GRAYSCALE)

HIEGHT = len(src_img_original)
WIDTH = len(src_img_original[0])
INF = WIDTH + HIEGHT # DE, D4, D8 중 가장 거리가 길게 잡히는 D4 기준으로도 W+H로 충분

# 사진 이진화 함수 : white(background) = 0, else(object) = 1
# cv2.threshold() 함수의 기능
def image_binaryization(image):
    for row in range(len(image)):
        for col in range(len(image[row])):
            if image[row][col] == WHITE:
                image[row][col] = 0
            else:
                image[row][col] = 1

src_img = src_img_original.copy()
image_binaryization(src_img)

# normalize 함수 : (거리) 최소값:최대값 = 0:255 로 정규화 해주는 함수
def image_normalization(image):
    maxVal = -1
    minVal = INF
    for i in range(HIEGHT):
        for j in range(WIDTH):
            if image[i][j] > maxVal:
                maxVal = image[i][j]
            if image[i][j] < minVal:
                minVal = image[i][j]
    
    for i in range(HIEGHT):
        for j in range(WIDTH):
            image[i][j] = int(255*(image[i][j] - minVal)/(maxVal-minVal))
    
            

            
### ----- 3가지 test 변수 : D4, D8, DE-----
# numpy.asarray()
dis_img_D_4 = src_img.copy().astype(numpy.uint32)
dis_img_D_8 = src_img.copy().astype(numpy.uint32)
dis_img_D_E = src_img.copy().astype(numpy.uint32)



### ----- D_4, D_8 : two_pass algorithm -----
for now_img, al_dis, br_dis in [(dis_img_D_4, [2,1,1,2], [2,1,1,2]), 
                                (dis_img_D_8, [1,1,1,1], [1,1,1,1])]:
    
    # 1. 오브젝트:0, 다른곳:무한
    for i in range(0, len(now_img)):
        for j in range(0, len(now_img[i])):
            if now_img[i][j] == 1:
                now_img[i][j] = 0
            else:
                now_img[i][j] = INF
    

    def hasINFval():
        for i in range(0, len(now_img)):
            for j in range(0, len(now_img[i])):
                if now_img[i][j] == INF:
                    return True
        else: return False

    while True:
        # 2-1. (top left) 에서 (bottom right)로 마스크 적용
        al_y = [-1, -1, 0, 1]
        al_x = [-1, 0, -1, -1]
        for i in range(HIEGHT):
            for j in range(WIDTH):
                # now_img[i][j] 에 대해 al 영역 마스크 적용
                for k in range(4):
                    ni = i + al_y[k]
                    nj = j + al_x[k]
                    # 경계로 인해 범위 밖은 continue
                    if ni<0 or nj<0 or ni>=HIEGHT or nj>=WIDTH:
                        continue
                    now_img[i][j] = min(now_img[i][j], now_img[ni][nj] + al_dis[k])

        # 2-2. (bottom right) 에서 (top left)로 마스크 적용
        br_y = [-1, 0, 1, 1]
        br_x = [1, 1, 0, 1]
        for i in reversed(range(HIEGHT)):
            for j in reversed(range(WIDTH)):
                # now_img[i][j] 에 대해 br 영역 마스크 적용
                for k in range(4):
                    ni = i + br_y[k]
                    nj = j + br_x[k]
                    # 경계로 인해 범위 밖은 continue
                    if ni<0 or nj<0 or ni>=HIEGHT or nj>=WIDTH:
                        continue
                    now_img[i][j] = min(now_img[i][j], now_img[ni][nj] + br_dis[k])
        
        # while문 탈출 조건: INF 없을 때
        if not hasINFval():
            break

    # normalize 하기
    image_normalization(now_img)

dis_img_D_4 = dis_img_D_4.astype(numpy.uint8)
dis_img_D_8 = dis_img_D_8.astype(numpy.uint8)
    


### ----- D_E, 유클리디안 거리 ----- 
# 두가지 방법: 1.openCV distanceTransform() 2. BFS알고리즘 (작은 이미지에서만 가능)
# 코드 최상단의 DE_LABEL 값으로 지정. dafault은 1번

if DE_LABEL == 1:
    src_img_gray = cv2.imread(OPEN_IMAGE_NAME, cv2.IMREAD_GRAYSCALE)
    _, threshold = cv2.threshold(src_img_gray, 122, 255, cv2.THRESH_BINARY)
    dis_img_D_E = cv2.distanceTransform(threshold, cv2.DIST_L2, 3)
    
    # normalize 하기
    image_normalization(dis_img_D_E)
    dis_img_D_E = dis_img_D_E.astype(numpy.uint8)

else:
    # 두 점 -> 유클리디안 (DE) 거리 리턴
    def D_Euclidean( pos1, pos2):
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) ** (1/2)

    # 점, img -> img에서 점의 오브젝트와 가장 가까운 거리 계산
    def bfs(pos, img):
        posY, posX = pos
        if img[posY][posX] == 1:
            return 0
        
        dy = [-1,1,0,0] # 상하좌우 y입장
        dx = [0,0,-1,1] # 상하좌우 x입장
        
        visited = [[False for i in range(WIDTH)] for j in range(HIEGHT)]
        visited[posY][posX] = True
        Q = deque([pos])
        while Q:
            nowY, nowX = Q.popleft()
            for k in range(4):
                newY = nowY + dy[k]
                newX = nowX + dx[k]
                
                # 범위 밖: continue
                if newY<0 or newX<0 or newY>=HIEGHT or newX>=WIDTH :
                    continue
                
                # 가장 가까운 오브젝트 위치 찾은 경우
                if img[newY][newX] == 1:
                    nPos = (newY, newX)
                    return D_Euclidean(pos, nPos) # 유클리디안 거리 리턴
                
                # 못찾은 경우, Q에 넣고 다시 반복
                if not visited[newY][newX]:
                    Q.append([newY, newX])
                    visited[newY][newX] = True
                

    # bfs 함수를 이용해 각 점마다 최단 거리를 찾고, img에 대입
    dis_img_D_E = dis_img_D_E.astype(numpy.float32)
    for i in range(HIEGHT):
        for j in range(WIDTH):
            distance = bfs((i, j), src_img)
            dis_img_D_E[i][j] = distance
            
    # normalize 하기
    image_normalization(dis_img_D_E)
    dis_img_D_E = dis_img_D_E.astype(numpy.uint8)
    
    
### ----- 이미지 파일 저장 -----
NEW_FILE_NAME = OPEN_IMAGE_NAME.split(".")
img_stack = numpy.hstack((src_img_original, dis_img_D_4, dis_img_D_8, dis_img_D_E))
cv2.imwrite(NEW_FILE_NAME[0] + "_src_d4_d8_de" + "." + NEW_FILE_NAME[1] , img_stack)


### ----- 시각화 -----
cv2.imshow("src, D4, D8, DE", img_stack)
cv2.waitKey(0)
cv2.destroyWindow("src, D4, D8, DE")

