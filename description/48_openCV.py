'''
pip install opencv-python

open source Computer vision

이미지 영상 처리 + 컴퓨터 비전 도구

이미지 처리
이미지 읽기/저장
크기 조절, 회전, 자르기
흑백변환, 블러처리
색상 추출

영상 & 웹캠
웹캠 실시간 영상 읽기
동영상 파일 재생
프레임 단위 처리

얼굴, 눈, 사람 검출
객체 / 얼굴 인식

'''
import cv2

img = cv2.imread("이미지경로")
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("cam", frame)
    if cv2.waitKey(1) == 27: # 키보드에서 27번 ESC키
        break

cap.release()
cv2.destroyAllWindows()

# 현재 나의 컴퓨터에서 웹캠이 실행