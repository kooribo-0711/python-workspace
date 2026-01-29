# 간단한 파이썬 계산기 프로그램

# 계산 함수 정의
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    # 0으로 나누는 경우 예외 처리
    if b == 0:
        return "0으로 나눌 수 없습니다."
    return a / b


# 계산기 메인 루프
while True:
    print("\n=== 파이썬 계산기 ===")
    print("1. 덧셈 (+)")
    print("2. 뺄셈 (-)")
    print("3. 곱셈 (*)")
    print("4. 나눗셈 (/)")
    print("5. 종료")

    # 사용자로부터 메뉴 선택 입력 받기
    choice = input("원하는 연산 번호를 선택하세요: ")

    # 종료 선택
    if choice == "5":
        print("계산기를 종료합니다.")
        break

    # 숫자 입력 받기
    try:
        num1 = float(input("첫 번째 숫자를 입력하세요: "))
        num2 = float(input("두 번째 숫자를 입력하세요: "))
    except ValueError:
        print("숫자만 입력해주세요!")
        continue

    # 선택한 연산 수행
    if choice == "1":
        result = add(num1, num2)
        print("결과:", result)

    elif choice == "2":
        result = subtract(num1, num2)
        print("결과:", result)

    elif choice == "3":
        result = multiply(num1, num2)
        print("결과:", result)

    elif choice == "4":
        result = divide(num1, num2)
        print("결과:", result)

    else:
        print("올바른 메뉴 번호를 선택해주세요.")
