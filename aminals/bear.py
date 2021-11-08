import dlib
import matplotlib.pyplot as plt # 결과를 나타내기 위함
import matplotlib.patches as patches
import cv2
from glob import glob

detector = dlib.cnn_face_detection_model_v1('bearface_network.dat')
predictor = dlib.shape_predictor('landmarkDetector.dat') #강아지 얼굴 인식하는 프로그램

#한 장일 경우
img = dlib.load_rgb_image('a.jpg') # 이미지를 rgb형태로 로드한다.
img_result = img.copy()

plt.figure(figsize=(16,10))
plt.imshow(img)

#여러장일 경우
# for img_path in glob('img/*.jpg'):
#     img = dlib.load_rgb_image(img_path)
#     img_result = img.copy()


dets = detector(img)# 이미지에서 얼굴 사각형 영역들을 찾아내서 dets에 저장
fig, ax = plt.subplots(1,figsize=(16,10))

for det in dets: # 얼굴이 여러개가 있을 수 있으므로 for문을 돌림
    x,y,w,h = det.rect.left(),det.rect.top(),det.rect.width(),det.rect.height()

    rect = patches.Rectangle((x,y),w,h,linewidth=3,edgecolor='r',facecolor='none') # 그래프영역에 직사각형을 그려줌
    ax.add_patch(rect)

    # shape = predictor(img,det,rect) # 랜드마크 6점을 구한다

    for point in rect():
        circle= patches.circle((point.x,point.y), radius=3, edgecolor='r',facedcolor='r')
        ax.add_patch(circle)

if len(rect)> 0:
    # 인식한 부분 표시하기
    print(rect)
    color = (0,0,255)
    for face in rect:
        x,y,w,h = face
        cv2.rectangle(img,(x,y),(x+w,y+h),color,thickness=8)
        # 파일로 출력하기
        cv2.imwrite("facedetech-output.PNG",img)
else:
    print("No face")
