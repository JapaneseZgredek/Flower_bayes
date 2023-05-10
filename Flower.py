class Flower:
    def __init__(self, list_of_attributes, flower_type):
        self.attributes = list_of_attributes
        self.flower_type = flower_type

    def calculate_distance(self, flower) -> float:
        distance = 0.0
        for i in range(len(self.attributes)):
            operation_minus = round(self.attributes[i] - flower.attributes[i], 5)
            power = round(operation_minus*operation_minus, 5)
            distance = round(distance + power, 5)
        return distance

    def change_commas_to_dots(self):
        for i in range(len(self.attributes)):
            self.attributes[i] = float(str(self.attributes[i]).replace(",", "."))

    def to_string(self):
        print(str(self.attributes) + " " + self.flower_type)
