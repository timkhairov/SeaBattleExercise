from unittest import TestCase
from field import Field, Point, Ship


class TestField(TestCase):
    def testField(self):
        field = Field(10, 10)
        print(field)
        print(Field.parseCoordinates("b5"))
        field.placeShip(Ship(3), "a0", "a2")
        print(field)
        print(field.getValue(Point(1, 1)))

        fireResult = field.fire("a1")
        print(fireResult)
        self.assertEqual(fireResult, "Wounded")

        fireResult = field.fire("b1")
        print(fireResult)
        self.assertEqual(fireResult, "Water")

        field.placeShip(Ship(1), "b1", "b1")
        fireResult = field.fire("b1")
        print(fireResult)
        self.assertEqual(fireResult, "Killed")


