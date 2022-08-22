class MONTH:
    def __class_getitem__(cls, key):
        if type(key) == str:
            return key[:3]
        else:
            raise Exception("Month transformation only allow string indexing")


class KT:
    def __class_getitem__(cls, key):
        if key not in {"0.162 para interiores", "0.190 para regiones costeras"}:
            raise Exception("Not in valid options")
        else:
            return float(key[:5])

class HEM:
    def __class_getitem__(cls, key):
        if key not in {"Norte","Sur"}:
            raise Exception("Not in valid options (North, South)")
        else:
            return key[0]

class LAT:
    def __class_getitem__(cls, key):
        try:
            key = int(key)
            return key
        except:
            raise Exception("Not a valid latitude")