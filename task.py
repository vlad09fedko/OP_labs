class Park:
    def __init__(self, address: str, length_of_bicycle_path: float, ticket_price: float):
        self.address = address
        self.length_of_bicycle_path = length_of_bicycle_path
        self.ticket_price = ticket_price

test = Park('Test address', 2000.5, 999.99)

for key, value in vars(test).items():
    print(f"{key}: {value}")
