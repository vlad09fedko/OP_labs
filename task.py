class Guest:
    def __init__(self, id: int, fullName: str, age: int, city: str, phone: str, gender: str):
        self.id = id
        self.fullName = fullName
        self.age = age
        self.city = city
        self.phone = phone
        self.gender = gender

    def check_phone_num(self):
        return True if self.phone.count('7') > 3 else False

class Party:
    def __init__(self, day: str, reason: str):
        self.day = day
        self.reason = reason

def findAvgAgeByGender(*guests: Guest, gender: str):
    count = 0
    sum = 0
    
    for guest in guests:
        if guest.gender == gender:
            count += 1
            sum += guest.age

    return sum / count

# AI test data
guests = [
    Guest(8, "Kateryna Melnyk", 27, "Ternopil", "+380681234567", "Female"),
    Guest(4, "Anna Tkachuk", 29, "Kharkiv", "+380677712345", "Female"),
    Guest(7, "Maksym Shevchenko", 31, "Zaporizhzhia", "+380997777777", "Male"), 
    Guest(1, "Oleksandr Ivanov", 28, "Kyiv", "+380671234567", "Male"),
    Guest(2, "Mariia Kovalenko", 34, "Lviv", "+380777771234", "Female"),    
    Guest(9, "Andrii Lysenko", 35, "Ivano-Frankivsk", "+380931234567", "Male"),
    Guest(3, "Ivan Petrenko", 22, "Odesa", "+380509876543", "Male"),
    Guest(10, "Viktoriia Kravchenko", 30, "Zhytomyr", "+380977234567", "Female"),
    Guest(5, "Dmytro Sydorenko", 41, "Dnipro", "+380971234777", "Male"),    
    Guest(6, "Olena Boiko", 25, "Vinnytsia", "+380631112233", "Female"),
]

for guest in guests:
    print(guest.id, guest.fullName, guest.check_phone_num())