class Park:
    def __init__(self, address: str, length_of_bicycle_path: float, ticket_price: float):
        self.address = address
        self.length_of_bicycle_path = length_of_bicycle_path
        self._ticket_price = ticket_price

    def __str__(self):
        str = ''
        for key, value in vars(self).items():
            str += f"{key}: {value}\n"
            
        return str


test1 = Park('Test1 address', 2000.5, 100)
print(test1)