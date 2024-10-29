class person:
    def __init__(self, name, gender, age):
        self.name = name
        self.age = age
        self.gender = gender
        self.info = name,age,gender
#    def greet(age):
#        if(age > 19):
#            print(f"안녕하세요,", {name}, "님은 성인이십니다.")
#        elif(age < 19):
#            print(f"안녕하세요,", {name}, "님은 미성년자이십니다.")


    def display(self):
        print('이름: '+self.name)
        print('나이: '+self.age)
        print('성별; ',self.gender)


name=str(input("이름을 입력하세요:"))
gender=str(input("성별을 입력하세요:"))
age=(input("나이를 입력하세요:"))

while True:
    if (gender=="male")|(gender=="female"):
        person=person(name,gender,age)
        break
    else:
        print("잘못된 성별을 입력하셨습니다.")
        gender=input("'male' 또는 'female'을 입력하세요: ")
        person=person(name,gender,age)


def display(self):
        print(f"이름 : {name}, 성별 : {gender}")
        print(int("나이 : {age}"))

#print(f'안녕하세요, {name}! {greet}이시군요!')

person.display()