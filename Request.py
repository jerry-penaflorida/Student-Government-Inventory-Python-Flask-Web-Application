class Request:
    def __init__(self, name, description, quantity, unit, email, status, request_number):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.unit = unit
        self.email = email
        self.status = status
        self.request_number = request_number
