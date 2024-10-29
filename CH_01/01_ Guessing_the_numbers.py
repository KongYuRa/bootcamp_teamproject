import random
number = random.randint(1,10)

print('안녕하세요. 1 부터 10 의 숫자 중 제가 생각하고 있는 숫자를 맞춰보세요.')

def game(start):
    while True:
        pick_number = int(input('숫자를 입력하세요: '))
        if pick_number == number:
            print('정답입니다!')
            break                 
        elif 11 > pick_number > number:
            print('다운! 다시 입력하세요: ')
        elif 0 < pick_number < number:
            print('업! 다시 입력하세요:')
        elif pick_number > 10:
            print('숫자가 너무 커요! 가장 큰 숫자는 10 입니다: ')
        elif pick_number < 1:
            print('숫자가 너무 작아요! 가장 작은 숫자는 1 입니다: ')

game(1)
while True:
    A=input("다시 한 번 해보고 싶다면 y를 입력해주세요: ")
    if A=="y":
        game(1)
    else:
        print("게임을 종료합니다!")
        break 