class BaseUnit(object):
    def get_point(self):
        raise NotImplementedError

    def has_point(self):
        raise NotImplementedError

    def set_point(self, point):
        raise NotImplementedError

    def del_point(self):
        raise NotImplementedError