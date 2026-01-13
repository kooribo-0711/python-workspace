'''

pip install pytesseract pillow

pillow
 - Python 이미지 처리 라이브러리
 - 이미지 파일을 열고, 크기조정, 변환 등을 처리
 - pytesseract 이미지를 전달하기 위해 필요
 - 아래 작성된 기능들과 별개로 이미지 관리할 때 가장 많이 사용하는 외부 라이브러리

pytesseract
 - google Tessract OCR 엔진을 Python에서 사용할 수 있게 해주는 레퍼
 - 파이썬 코드 안에서 Tesseract 프로그램을 이용해서 글자를 인식하고 추출

Tesseract 
 - 구글이 만든 무료 OCR(글자인식) 프로그램.
 - 이미지 속 글자를 텍스트로 바꿔줌
 - 100개 이상 언어 지원


OCR : Optical Character Recognition : 광학 문자 인식
 - 사진/이미지 속 글자를 컴퓨터가 읽을 수 있는 텍스트로 바꿔주는 기술
 - 네이버 파파고 사진번역
 - 카카오톡 이미지 속 텍스트 복사
 - 은행 앱 신분증 스캔
등 다양한 회사에서 사용

'''

'''
pillow
 - 이미지 열기/저장 크기조정 자르기 회전 반전 필터효과 색상변환 그리기 등등...

Image.open("이미지파일.확장자명칭") : 이미지 열기
Image.open("이미지파일.확장자명칭").save("이미지파일.확장자명칭") : 이미지 저장
Image.open("이미지파일.확장자명칭").resize(가로크기,세로크기) : 크기변경
Image.open("이미지파일.확장자명칭").crop(왼,위,오른,아래) : 이미지 자르기
Image.open("이미지파일.확장자명칭").convert("L") : 흑백변환
'''

from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance

def 이미지_열기_저장():
    img = Image.open("tesseract.jpg")
    img.save("tesseract1.png")
# 이미지_열기_저장()

def 이미지_필터_적용():
    # 파일이 존재하지 않을 경우 에러 발생하므로
    # 나중에 파일이 만약에 존재한다면 경우를 추가하여
    # 파일이 존재할 경우에만 이미지를 사용할 수 있도록 설정
    # Image.open("tesseract1.png").filter(ImageFilter.BLUR).save("tesseract_blur_filter.png)")
    사진_가져오기 = Image.open("tesseract.jpg")
    블러필터적용 = 사진_가져오기.filter(ImageFilter.BLUR).save("tesseract_blur_filter.png")
    사진_가져오기.filter(ImageFilter.SHARPEN).save("tesseract_sharpen_filter.png")
    사진_가져오기.filter(ImageFilter.FIND_EDGES).save("tesseract_find_edge_filter.png")
    사진_가져오기.filter(ImageFilter.SMOOTH).save("tesseract_smooth_filter.png")
    print("모든 필터 적용이 완료되었습니다")
    # 사진을 저장할 때, 동일한 명칭이 존재할 경우 -> 덮어쓰기 된다.
# 이미지_필터_적용()

def 색상변환():
    img = Image.open("dog.jpg")

    # === 주요모드 ===
    # 1. 흑백 (GrayScale)
    gray = img.convert("L")
    gray.save("dog_gray.jpg")
    
    # 2. RGB (일반컬러)
    rgb = img.convert("RGB")
    rgb.save("dog_RGB.jpg")

    # 3. RGBA (투명도 포함)
    rgba = img.convert("RGBA")
    # jpg는 투명도를 지원하지 않기 때문에 png 파일로만 저장 가능
    # png 파일은 배경을 투명하게 할 수 있지만 jpg는 투명함 자체가 없음
    # 배경 투명하게 만든 이미지를 jpg 변경하면 투명한 공간을 흰색 채워짐
    # rgba.save("dog_RGBA.jpg")
    rgba.save("dog_RGBA.png")
    # 4. 완전 흑백
    bw = img.convert("1")
    bw.save("dog_black_white.jpg")
    # jpg jpeg = 초기 컴퓨터가 만들어졌을 때 확장자 명칭을 3글자 이상 불가
    # txt png jpg doc
    # 컴퓨터가 발전하며 확장자 명칭의 글자수 제한을 해지
    # 확장자 .jpeg .docs .excel 과 같은 확장자명칭을 사용할 수 있게 됨
    # 즉 jpg = jpeg
# 색상변환()

def 색상조정():
    # 이미지 밝게 조절한 상태를 확인하고 싶지만 저장은 하고싶지 않을 때 사용
    img = Image.open("dog.jpg")
    밝기조정 = ImageEnhance.Brightness(img) # 이미지 밝기를 조정 설정
    밝게 = 밝기조정.enhance(1.5) # 이미지 밝기를 1.5배 밝게
    # 밝게.show() # 밝게 조절한 이미지 미리보기
    어둡게 = 밝기조정.enhance(0.5) # 이미지 밝기를 0.5배 어둡게
    # 어둡게.show() # 어둡게 조절한 이미지 미리보기
    # 한번에 모든 기능을 작성할 경우 변수 공간에 데이터를 저장하지 않고 바로 사용 가능하나
    # 아래에서 담아놓은 데이터를 재사용할 수 없음. 담아놓은 데이터가 없으며, 일회용 데이터로 사용했기 때문
    # ImageEnhance.Contrast(img).enhance(2.0).show() # 대비 높게 설정

    어두운_대비조절_이미지 = ImageEnhance.Contrast(img).enhance(0.5)
    # 어두운_대비조절_이미지.show()

    선명_조절_이미지 = ImageEnhance.Sharpness(img)
    # 선명_조절_이미지.enhance(2.0).show()

    채도_조절 = ImageEnhance.Color(img)
    비비드채도 = 채도_조절.enhance(2.0) # vivid = 선명하게
    파스텔채도 = 채도_조절.enhance(0.5)
    비비드채도.show()
    파스텔채도.show()
    # 이미지에 필터를 적용할 때 적용된 필터 사진이 매 순간 저장되는 것이 아니라
    # 저장되기 전에 이미지 상태 확인하기
# 색상조정()

'''
    이미지향상    밝기조절  (밝기조절할 이미지 가져오기)
    ImageEnhance.Brightness(Image.open("dog.jpg"))

    이미지향상    밝기조절  (밝기조절할 이미지 가져오기).밝기를 1,5배 증가
    ImageEnhance.Brightness(Image.open("dog.jpg")).enhance(1.5)
    이미지향상    밝기조절  (밝기조절할 이미지 가져오기).밝기를 50% 감소
    ImageEnhance.Brightness(Image.open("dog.jpg")).enhance(0.5)
 
    이미지향상    대비조절  (대비조절할 이미지 가져오기).대비 2배 증가
    ImageEnhance.Contrast(Image.open("dog.jpg")).enhance(2.0)
    이미지향상    대비조절  (대비조절할 이미지 가져오기).대비 50% 감소
    ImageEnhance.Contrast(Image.open("dog.jpg")).enhance(0.5)
    
    이미지향상    선명도조절  (선명도 조절할 이미지 가져오기).
    ImageEnhance.Sharpness(Image.open("dog.jpg")).enhance(2.0)

    이미지향상    채도조절  (채도조절할 이미지 가져오기).
    ImageEnhance.Color(Image.open("dog.jpg")).enhance(2.0)
    ImageEnhance.Color(Image.open("dog.jpg")).enhance(0.5)
    
    보통 이미지 원본 1.0 or 100
    
'''

def 인스타그램_필터():
    이미지_가져오기 = Image.open("dog.jpg")
    # 대비 조절 후 대비조절 문제는 없지만, 파일이 대비조절하면 사용되거나 그럴 경우
    # 코드가 동일한 기능에서 중첩되는 현상이 발생할 수 있으므로
    # try catch 상태 예외 설정을 잰행하여 중복도 가능할 수 있도록
    # 발생하는 모든 에러에 대하여 개발자는 당황하지 않고, 예외처리를 할 수 있도록
    # 클라이언트보다 모든 에러를 먼저 찾는다.
    대비조절 = ImageEnhance.Contrast(이미지_가져오기).enhance(1.3)
    채도조절 = ImageEnhance.Color(대비조절).enhance(1.2)
    밝기조절 = ImageEnhance.Brightness(채도조절).enhance(1.1)
    밝기조절.save("인스타그램1.jpg")
# 인스타그램_필터()

def 인스타그램_클라이언트_조절():
    try :
        입력파일 = input("원본 이미지 파일 이름을 입력하세요 (예: dog.jpg) : ")
        출력파일 = input("저장할 파일 이름을 입력하세요 (예: 결과물.jpg) : ")

        # input = 문자열 = String이기 때문에
        # 입력받은 문자열을 float로 소수점이 존재하는 숫자형태로 변환
        대비 = float(input("대비 조절 값 (1.0 = 원본, 추천 : 1.3) : "))
        채도 = float(input("채도 조절 값 (1.0 = 원본, 추천 : 1.2) : "))
        밝기 = float(input("밝기 조절 값 (1.0 = 원본, 추천 : 1.1) : "))

        이미지_가져오기 = Image.open(입력파일)

        대비조절 = ImageEnhance.Contrast(이미지_가져오기).enhance(대비)
        채도조절 = ImageEnhance.Color(대비조절).enhance(채도)
        밝기조절 = ImageEnhance.Brightness(채도조절).enhance(밝기)
        밝기조절.save(출력파일)
        print("필터가 적용되었습니다.")
    except FileNotFoundError:
        print(f"에러 : {입력파일} 파일을 찾을 수 없습니다.")
    except ValueError:
        print(f"에러 : 확장자 이름이나 숫자를 올바르게 입력해주세요.")
    except Exception as e:
        print(f"개발자가 눈치채지 못한 처음 보는 에러 : {e} ")
    # FileNotFoundError 와 ValueError는 개발자가 클라이언트가 요구한 대로 데이터를 작성하지 않았을 때 클라이언트에게 고지
    # Exception은 개발자도 처음보는 예외상황
    # 이러한 예외상항을 log에서 확인하고 예외상황에 따른 대처를 작성해야 한다.
인스타그램_클라이언트_조절()

