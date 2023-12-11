from json import JSONEncoder, JSONDecoder, dump, loads


# define the Encoder class used in serialization
class Encoder(JSONEncoder):
    # from a Python object we need to obtain a json representation
    def default(self, o: str) -> str:
        return o.__dict__


class Decoder(JSONDecoder):
    # We have to transform the serialized string into Python objects
    def decode(self, o):
        data = loads(o)
        vals = []
        for key in data.keys():
            vals.append(data[key])
        cat = Category(*vals)
        return cat


class Category:
    # define the Category class which holds the categories of products
    def __init__(self, name) -> object:
        self.name = name

    def __eq__(self, other) -> bool:
        # Overloaded in order to verify the membership inside a collection
        if type(other) == type(self):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)
