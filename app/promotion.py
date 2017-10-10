from datetime import datetime

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Promotion:

    data = []

    def __init__(self, name='', promo_type='', value=0, start_date=datetime.max, end_date=datetime.max, detail=''):
        """ Initialize a Promotion """
        self.id = id(self)
        self.name = name
        self.promo_type = promo_type
        self.value = value
        self.start_date = start_date
        self.end_date = end_date
        self.detail = detail
    
    def save(self):
        """ Add a Promotion to the collection """
        Promotion.data.append(self)

    def delete(self):
        """ Removes a Promotion from the collection  """
        Promotion.data.remove(self)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "promo_type": self.promo_type,
            "value": self.value,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "detail": self.detail    
        }

    @staticmethod
    def __validate_promo_data(data):
        """ 
            validate data of promo
        """
        pass

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary
        Args:
            data (dict): A dictionary containing the Promotion data
        """
        Promotion.__validate_promo_data(data)

    @staticmethod
    def all():
        return [promo for promo in Promotion.data]

    @staticmethod
    def find(conditions):
        """ conditions is a dictionary including all requirement for finding promos """
        Promotion.__validate_promo_data(conditions)

    @staticmethod
    def find_by_id(id):
        """ Finds a Pet by it's ID """
        if not Promotion.data:
            return None
        promos = [promo for promo in Promotion.data if promo.id == id]
        if promos:
            return promos[0]
        return None
