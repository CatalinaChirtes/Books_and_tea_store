from json import JSONEncoder, JSONDecodeError, loads, dump
import product


# define the Encoder class used in serialization
class Encoder(JSONEncoder):
    # from a Python object we need to obtain a json representation
    def default(self, o):
        return o.__dict__


class Products:
    # holds a list with all Product objects
    products = []

    @classmethod
    def load_products(cls):
        decoder = product.Decoder()
        try:
            with open("products.txt") as f:
                for line in f:
                    data = loads(line)
                    decoded_product = decoder.decode(data)
                    if decoded_product not in cls.products:
                        cls.products.append(decoded_product)
        except (JSONDecodeError, FileNotFoundError) as e:
            cls.products = []
        return cls.products

    @classmethod
    def remove_product(cls, prod):
        cls.load_products()
        for productel in cls.products:
            if prod == productel.name:
                cls.products.remove(productel)
                with open("products.txt", 'w') as f:
                    for prod in cls.products:
                        e = Encoder()
                        encoded_prod = e.encode(prod)
                        dump(encoded_prod, f)
                        f.write("\n")
                return True
        else:
            print("\nThis product doesn't exist. Please type a different one.")
            return False

    @classmethod
    def add_product(cls, prod):
        cls.load_products()
        if prod not in cls.products:
            with open("products.txt", 'a') as f:
                e = Encoder()
                encoded_prod = e.encode(prod)
                dump(encoded_prod, f)
                f.write("\n")
            return True
        else:
            print("\nThis product already exists. Please type a different one.")
            return False

    @classmethod
    def update_product_stock(cls, prod, amount):
        cls.load_products()
        for existing_product in cls.products:
            if existing_product == prod:
                if existing_product.stock == 0:
                    print("The product is not in stock anymore.")
                    return
                else:
                    existing_product.stock = prod.stock - int(amount)
                    if existing_product.stock < 0:
                        print("The stock is insufficient. You can't order this many products.")
                    else:
                        cls.remove_product(prod.name)
                        prod.stock = existing_product.stock
                        cls.add_product(prod)
