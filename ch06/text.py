class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __getitem__(self, key):
        if key in [0, -3]:
            return self.x
        elif key in [1, -2]:
            return self.y
        elif key in [2, -1]:
            return self.z
        else:
            raise IndexError("Index out of range")


if __name__ == "__main__":
    v = Vector(1, 2, 3)
    print(v)
    print(abs(v))
    print(bool(v))
