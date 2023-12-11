from json import JSONEncoder, JSONDecodeError, loads, dump
import order
from products import Products


# define the Encoder class used in serialization
class Encoder(JSONEncoder):
    # from a Python object we need to obtain a json representation
    def default(self, o):
        return o.__dict__


class Orders:
    # holds a list with all Order objects
    orders = []

    @classmethod
    def load_orders(cls):
        cls.orders = []
        decoder = order.Decoder()
        try:
            with open("orders.txt") as f:
                for line in f:
                    data = loads(line)
                    decoded_order = decoder.decode(data)
                    cls.orders.append(decoded_order)
        except (JSONDecodeError, FileNotFoundError) as e:
            cls.orders = []
        return cls.orders

    @classmethod
    def add_order(cls, ord):
        cls.load_orders()
        if ord not in cls.orders:
            cls.orders.append(ord)
            with open("orders.txt", 'a') as f:
                e = Encoder()
                encoded_ord = e.encode(ord.serialize())
                for prod in ord.ordered_products:
                    Products.update_product_stock(prod, ord.ordered_products[prod])
                dump(encoded_ord, f)
                f.write("\n")
            return True
        else:
            return False

    @classmethod
    def refresh_orders(cls):
        cls.orders = []
        cls.load_orders()
