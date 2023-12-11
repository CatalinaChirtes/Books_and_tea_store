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
        ord = Order(*vals)
        return ord


class Order:
    def __init__(self, ordered_products, buyer_name, destination_address):
        self.ordered_products = ordered_products
        self.buyer_name = buyer_name
        self.destination_address = destination_address

    def __eq__(self, other) -> bool:
        if type(other) == type(self):
            return self.ordered_products == other.ordered_products \
               and self.buyer_name == other.buyer_name \
               and self.destination_address == other.destination_address

    def __hash__(self):
        return hash(self.ordered_products.items())

    def serialize(self):
        serialized_products = {
            prod.name: {'amount': self.ordered_products[prod]}
            for prod in self.ordered_products
        }
        return {
            'ordered_products': serialized_products,
            'buyer_name': self.buyer_name,
            'destination_address': self.destination_address
        }
