class Guest:
    def __init__(self, id: int, name: str, age: int, city: str, phone: str, gender: enumerate):
        self.id = id
        self.name = name
        self.age = age
        self.city = city
        self.phone = phone
        self.gender = gender

    def check_phone_number(self):
        if self.phone.count('7') > 3:
            self.is_lucky_phone_number = True

class Party:
    def __init__(self, day: str, reason: str):
        self.day = day
        self.reason = reason

# def findAvgAgeByGender(*guests, gender: str):
#     sum = 0
#     for guest in guests:
#         if guest.gender == gender:
            
    
        
