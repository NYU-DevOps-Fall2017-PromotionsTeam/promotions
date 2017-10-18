from datetime import datetime


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing and querying """
    pass


class Promotion:

    data = []

    def __init__(self):
        """ Initialize a Promotion """
        self.id = id(self)
        self.name = 'default'
        self.promo_type = '$'
        self.value = 0.0
        self.start_date = datetime.max
        self.end_date = datetime.max
        self.detail = 'n/a'

    def save(self):
        """ Add a Promotion to the collection """
        Promotion.data.append(self)

    def delete(self):
        """ Removes a Promotion from the collection  """
        if self in Promotion.data:
            Promotion.data.remove(self)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "promo_type": self.promo_type,
            "value": self.value,
            "start_date": self.start_date.isoformat(sep=' ', timespec='seconds'),
            "end_date": self.end_date.isoformat(sep=' ', timespec='seconds'),
            "detail": self.detail
        }

    @staticmethod
    def __validate_data(data):
        if not isinstance(data, dict):
            raise DataValidationError(
                'Invalid promo: body of request contained bad or no data.')
        if 'name' in data:
            data['name'] = str(data['name'])
        if 'promo_type' in data and data['promo_type'] not in ['$', '%']:
            raise DataValidationError(
                'Invalid promo: invalid promo type, $ or % required.')
        if 'detail' in data:
            data['detail'] = str(data['detail'])

    @staticmethod
    def __validate_promo_data(data):
        """ 
            validate data of promo
        """
        Promotion.__validate_data(data)
        if 'value' in data:
            try:
                data['value'] = float(data['value'])
            except ValueError as e:
                raise DataValidationError(
                    'Invalid promo: invalid value, number required. ' + e.args[0])
        if 'start_date' in data:
            try:
                data['start_date'] = datetime.strptime(
                    data['start_date'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise DataValidationError(
                    'Invalid promo: invalid start date format, date format required: YYYY-MM-DD HH:MM:SS. ' + e.args[0])
        if 'end_date' in data:
            try:
                data['end_date'] = datetime.strptime(
                    data['end_date'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise DataValidationError(
                    'Invalid promo: invalid end date format, date format required: YYYY-MM-DD HH:MM:SS. ' + e.args[0])

    @staticmethod
    def __validate_query_data(data):
        Promotion.__validate_data(data)
        if 'valid_on' in data:
            try:
                data['valid_on'] = datetime.strptime(
                    data['valid_on'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise DataValidationError(
                    'Invalid promo: invalid valid_on format, date format required: YYYY-MM-DD HH:MM:SS. ' + e.args[0])
        if 'discount_greater_or_equal' in data:
            try:
                data['discount_greater_or_equal'] = float(
                    data['discount_greater_or_equal'])
            except ValueError as e:
                raise DataValidationError(
                    'Invalid promo: invalid discount_greater_or_equal, number required. ' + e.args[0])

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary
        Args:
            data (dict): A dictionary containing the Promotion data
        """
        Promotion.__validate_promo_data(data)
        if 'name' in data:
            self.name = str(data['name'])
        if 'promo_type' in data:
            self.promo_type = data['promo_type']
        if 'value' in data:
            self.value = data['value']
        if 'start_date' in data:
            self.start_date = data['start_date']
        if 'end_date' in data:
            self.end_date = data['end_date']
        if 'detail' in data:
            self.detail = str(data['detail'])

    @staticmethod
    def all():
        '''Return all promotions in the db'''
        return [promo for promo in Promotion.data]

    @staticmethod
    def query(filters):
        """ filters is a dictionary including all requirement for finding promos """
        Promotion.__validate_query_data(filters)
        result = set(Promotion.data)
        if 'name' in filters:
            result &= set(
                [promo for promo in Promotion.data if filters['name'] in promo.name])
        if 'promo_type' in filters:
            result &= set(
                [promo for promo in Promotion.data if promo.promo_type == filters['promo_type']])
        if 'detail' in filters:
            result &= set([promo for promo in Promotion.data if filters[
                          'detail'] in promo.detail])
        if 'valid_on' in filters:
            result &= set([promo for promo in Promotion.data if filters[
                          'valid_on'] >= promo.start_date and filters['valid_on'] < promo.end_date])
        if 'discount_greater_or_equal' in filters:
            result &= set([promo for promo in Promotion.data if promo.value >= filters[
                          'discount_greater_or_equal']])
        return list(result)

    @staticmethod
    def find_by_id(promo_id):
        """ Finds a Promo by it's ID """
        return [promo for promo in Promotion.data if promo.id == promo_id]
