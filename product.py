from json import JSONEncoder, JSONDecoder, loads


# define the Encoder class used in serialization
class Encoder(JSONEncoder):

    def default(self, o: object) -> object:
        return o.__dict__


class Decoder(JSONDecoder):
    def decode(self, o):
        data = loads(o)
        vals = []
        for key in data.keys():
            vals.append(data[key])
        prod = Product(*vals)
        return prod


# define the Product class, which is the base class for all the  products in the store
class Product:
    def __init__(self, name, category, stock):
        self.name = name
        self.category = category
        self.stock = int(stock)

    def __eq__(self, other) -> bool:
        if type(other) == type(self):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)
