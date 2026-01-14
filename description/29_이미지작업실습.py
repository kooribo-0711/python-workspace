####################
## 이미지 포맷 변환
####################
# dog.jpg 파일을 열어서 dogs.png 형식으로 저장하는 함수를 만들기
# 함수이름 : 이미지_확장자_변환()
####################
## 밝은 이미지 사진 만들기
####################
# dog.jpg 파일을 2배로 밝게 만들어 저장하는 함수 만들기
# 함수이름 : 이미지_밝게만들기()
# 밝기조절: 2.0배
# 저장파일명 : dog_bright_2.0.png
# 참고로 맨 마지막에 존재하는 . 이외의 점들은 모두 파일명칭으로 사용됨
####################
## 필터 세트
####################
# dog.jpg 파일에 세가지 필터를 적용해서 저장하는 함수 만들기
# 함수이름 : 필터_세트()
# 선명도 -> Sharpness Blur Smooth
# 보통 
# 흐림효과 1.3 선명효과 1.5 채도조절 2.35
# 저장파일명 : dog_filter.png

from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance

def 이미지_확장자_변환():
    img = Image.open("dog.jpg")
    img.save("dogs1.png")
    print("확장자가 변환되었습니다.")
이미지_확장자_변환()

def 이미지_밝게_만들기():
    img = Image.open("dog.jpg")
    밝기조정 = ImageEnhance.Brightness(img).enhance(2.0) # 이미지 밝기를 조정 설정
    밝기조정.save("dog_bright1_2.0.png")
    print("이미지가 밝아졌습니다.")
이미지_밝게_만들기()

def 필터_세트():
    img = Image.open("dog.jpg")
    흐림효과 = img.filter(ImageFilter.GaussianBlur(radius=1.3))
    선명효과 = ImageEnhance.Sharpness(흐림효과).enhance(1.5)
    채도조절 = ImageEnhance.Color(선명효과).enhance(2.35)
    채도조절.save("dog_filter1.png")
    print("필터가 적용되었습니다.")
필터_세트()