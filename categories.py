from json import JSONEncoder, JSONDecodeError, loads, dump
import category


# define the Encoder class used in serialization
class Encoder(JSONEncoder):
    # from a Python object we need to obtain a json representation
    def default(self, o):
        return o.__dict__


class Categories:
    # holds a list with all Category objects
    categories = []

    @classmethod
    def load_categories(cls):
        decoder = category.Decoder()
        try:
            with open("categories.txt") as f:
                for line in f:
                    data = loads(line)
                    decoded_category = decoder.decode(data)
                    if decoded_category not in cls.categories:
                        cls.categories.append(decoded_category)
        except (JSONDecodeError, FileNotFoundError) as e:
            cls.categories = []
        return cls.categories

    @classmethod
    def remove_category(cls, cat):
        cls.load_categories()
        if cat in cls.categories:
            cls.categories.remove(cat)
            with open("categories.txt", 'w') as f:
                for cat in cls.categories:
                    e = Encoder()
                    encoded_cat = e.encode(cat)
                    dump(encoded_cat, f)
                    f.write("\n")
            return True
        else:
            print("\nThis category doesn't exist. Please type a different one.")
            return False

    @classmethod
    def add_category(cls, cat):
        cls.load_categories()
        if cat not in cls.categories:
            with open("categories.txt", 'a') as f:
                e = Encoder()
                encoded_cat = e.encode(cat)
                dump(encoded_cat, f)
                f.write("\n")
            return True
        else:
            print("\nThis category already exists. Please type a different one.")
            return False
