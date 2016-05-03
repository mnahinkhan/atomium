from .exceptions import InvalidElementError

class Atom:

    def __init__(self, x, y, z, element):
        for coordinate in (x, y, z):
            if not isinstance(coordinate, float):
                error_message = "'%s' is not a valid coordinate" % str(coordinate)
                raise TypeError(error_message)
        if not isinstance(element, str):
            error_message = "'%s' is not a valid element" % str(element)
            raise TypeError(error_message)
        if len(element) == 0:
            error_message = "An Atom's element cannot be an empty string"
            raise InvalidElementError(error_message)
        elif len(element) >= 2:
            error_message = "'%s' is not a valid element" % element
            raise InvalidElementError(error_message)
        self.x = x
        self.y = y
        self.z = z
        self.element = element


    def __repr__(self):
        return "<Atom (%s)>" % self.element
