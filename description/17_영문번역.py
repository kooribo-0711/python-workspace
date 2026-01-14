'''

pip install googletrans==4.0.0-rc1
    번역에서 가장 원조
    rc1 정식으로 버전을 내기 전에 테스트 버전으로 사용
    Google Translate API를 무료로 사용해서 번역 가능
    2020년에 개발 중단 == Python 3.9
    Python3.12에서는 심하게 불안정
    최신 파이썬에는 사용을 잘 하지 않음

pip install deep-translator
    튀지니 출신 엔지니어가 googletrans가 불안정해지자 더 안정적이고 다양한 번역 서비스를 진행하는 라이브러리 개발
    누구나 소스코드를 보고 기여할 수 있도록 코드를 오픈
    라이브러리 : 특정 기능에 특화된 도구 모음

pip install googletrans-py
    구글이 개발을 중단하여 기존의 구글에서 개발하던 googletrans를 복사하여 만든 복사본. 구글에서 만든게 아님
    현재는 deep-translator보다 안정적이지 않음

'''
# deep-translator 라이브러리에서 GoogleTranslator 라는 도구를 활용하여 번역을 진행하겠다.
from deep_translator import GoogleTranslator


text = "Hello World"
# 결과 = GoogleTranslator(source='en', target='ko').translate(text)
결과 = GoogleTranslator(source='en', target='ja').translate(text)
print(결과)

text1 = "안녕하세요"
# 결과 = GoogleTranslator(source='en', target='ko').translate(text)
결과2 = GoogleTranslator(source='auto', target='en').translate(text1)
print(결과2)

'''
def 만능번역기() :
    print("번역할 문장과 언어를 입력하시오.")
    번역할문장 = input("번역할 문장을 입력하시오.")
    번역할언어 = input("번역할 언어를 입력하시오.")

    결과 = GoogleTranslator(source='auto', target={번역할언어}).translate(번역할문장)
    print(결과)

만능번역기()
'''


'''
GoogleTranslate().translate()

구글번역기능()
 .         내부에 존재하는 기능들 중에서
 translate()라는 기능을 사용하겠다.

.기능명칭() = 특정 변수나, 특정 기능에서만 사용되는 기능

GoogleTranslator() 기능 내부에서 translate() 기능이 정의되었으며
GoogleTranslator().translate() = 구글변역기능 내부에 존재하는 translate() 기능을 사용하겠다.


GoogleTranslator(source='대소문자 상관없음', target'대소문자 상관없음').translate('문장')
구글번역기같은가능(원래 문장은 ㅐㅐ 나라 언어로 되어있고, ㅇㅇ 나라 언어로 변경할 것이다.).변환기능('언어변경할문장')

source = 'auto' 사용 가능
          auto 문장을 보고 어떤 나라의 언어인지 언어를 알아서 감지하겠다.

                   원본언어     목표언어   번역실행기능("번역할문장")
GoogleTranslator(source='en', target='ja').translate("번역될문자열")

'''

