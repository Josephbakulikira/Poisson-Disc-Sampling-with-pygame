import math
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def normalize_vector(self):
        magnitude = math.sqrt(self.x * self.x + self.y * self.y)
        self.x = self.x/magnitude
        self.y = self.y/magnitude


    def set_magnitude(self, new_magnitude):
        self.normalize_vector()
        x = self.x * new_magnitude
        y = self.y * new_magnitude

        return Vector2(x, y)
