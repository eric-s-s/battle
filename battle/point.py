
class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not self == other

    def north(self):
        return Point(self._x, self._y + 1)

    def south(self):
        return Point(self._x, self._y - 1)

    def east(self):
        return Point(self._x + 1, self._y)

    def west(self):
        return Point(self._x - 1, self._y)

    def plus(self, x, y):
        return Point(self._x + x, self._y + y)

    def plus_x(self, x):
        return self.plus(x, 0)

    def plus_y(self, y):
        return self.plus(0, y)

    def at_distance(self, distance):
        if distance == 0:
            return [self]
        out = []
        for del_x in range(distance + 1):
            del_y = distance - del_x
            if not del_x:
                out.append(self.plus_y(del_y))
                out.append(self.plus_y(- del_y))
            elif not del_y:
                out.append(self.plus_x(del_x))
                out.append(self.plus_x(- del_x))
            else:
                out.append()




