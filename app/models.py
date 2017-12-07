import os
import json
import logging
import pickle
from cerberus import Validator
from redis import Redis
from redis.exceptions import ConnectionError
from datetime import datetime

######################################################################
# Custom Exceptions
######################################################################


def validate_datetime(field, value, error):
    try:
        datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        error(field, "Datetime format must be YYYY-MM-DD HH:MM:SS")


def get_timestamp(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').timestamp()


class DataValidationError(ValueError):
    pass


class DatabaseConnectionError(ConnectionError):
    pass


class Promotion:

    logger = logging.getLogger(__name__)
    redis = None

    schema = {
        'name': {'type': 'string'},
        'promo_type': {'type': 'string', 'allowed': ['%', '$']},
        'value': {'type': 'number', 'min': 0},
        'start_date': {'type': 'string', 'validator': validate_datetime},
        'end_date': {'type': 'string', 'validator': validate_datetime},
        'detail': {'type': 'string'}
    }
    __validator = Validator(schema)
    __validator.allow_unknown = True

    def __init__(self, promo_id=None):
        """ Initialize a Promotion """
        self.id = promo_id or id(self)
        self.name = 'default'
        self.promo_type = '$'
        self.value = 0.0
        self.start_date = '9999-12-31 23:59:59'
        self.end_date = '9999-12-31 23:59:59'
        self.detail = 'n/a'

    def save(self):
        """ Add a Promotion to the collection """
        Promotion.redis.set(Promotion.key(self.id),
                            pickle.dumps(self.serialize()))
        self.add_to_xxx()

    def delete(self):
        """ Removes a Promotion from the collection  """
        Promotion.redis.delete(Promotion.key(self.id))
        self.remove_from_xxx()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "promo_type": self.promo_type,
            "value": self.value,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "detail": self.detail
        }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary
        Args:
            data (dict): A dictionary containing the Promotion data
        """
        if isinstance(data, dict) and Promotion.__validator.validate(data):
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
        else:
            raise DataValidationError(
                'Invalid Promotion data: ' + str(Promotion.__validator.errors))
        return self

    @staticmethod
    def key(value):
        """ Creates a Redis key using class name and value """
        return 'promotion:{}'.format(value)

    @staticmethod
    def remove_all():
        """ Removes all Promotions from the database """
        Promotion.redis.flushall()

    @staticmethod
    def all():
        """ Query that returns all Promotions """
        # results = [Promotion.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in Promotion.redis.scan_iter(Promotion.key('*')):
            data = pickle.loads(Promotion.redis.get(key))
            promotion = Promotion(data['id']).deserialize(data)
            results.append(promotion)
        return results

######################################################################
#  R E L A T I O N S H I P S
######################################################################

    def add_to_xxx(self):
        """ Adds the Promotions Redis key to a promo_type set, ordered Start Date and End Date set"""
        Promotion.redis.sadd('promo_type:{}'.format(
            self.promo_type), Promotion.key(self.id))
        Promotion.redis.zadd('start_date', Promotion.key(
            self.id), get_timestamp(self.start_date))
        Promotion.redis.zadd('end_date', Promotion.key(
            self.id), get_timestamp(self.end_date))

    def remove_from_xxx(self):
        """ Removes the Promotions Redis key from a Category set, ordered Start Date and End Date set"""
        Promotion.redis.srem('promo_type:{}'.format(
            self.promo_type), Promotion.key(self.id))
        Promotion.redis.zrem('start_date', Promotion.key(self.id))
        Promotion.redis.zrem('end_date', Promotion.key(self.id))

    @staticmethod
    def find_by_id(promo_id):
        """ Finds a Promo by it's ID """
        """ Query that finds Promotions by their id """
        key = Promotion.key(promo_id)
        if Promotion.redis.exists(key):
            data = pickle.loads(Promotion.redis.get(key))
            promo = Promotion(data['id']).deserialize(data)
            return promo
        return None

    @staticmethod
    def find_by_conditions(conditions):
        keys = None
        if 'promo_type' in conditions:
            keys = Promotion._find_by_promo_type(conditions['promo_type'])
        if 'available_on' in conditions:
            available = Promotion._find_by_available_on(
                conditions['available_on'])
            if keys is not None:
                keys = keys & available
            else:
                keys = available
        results = []
        if keys:
            for k in keys:
                data = pickle.loads(Promotion.redis.get(k))
                results.append(Promotion(data['id']).deserialize(data))
            return results
        return []

    @staticmethod
    def _find_by_promo_type(promo_type):
        return set(Promotion.redis.smembers('promo_type:' + promo_type))

    @staticmethod
    def _find_by_available_on(date_str):
        timestamp = get_timestamp(date_str)
        start_keys = set(Promotion.redis.zrangebyscore(
            'start_date', '-inf', timestamp))
        end_keys = set(Promotion.redis.zrangebyscore(
            'end_date', '(' + str(timestamp), '+inf'))
        return start_keys & end_keys

    ######################################################################
    #  R E D I S   D A T A B A S E   C O N N E C T I O N   M E T H O D S
    ######################################################################

    @staticmethod
    def connect_to_redis(hostname, port, password):
        """ Connects to Redis and tests the connection """
        Promotion.logger.info("Testing Connection to: %s:%s", hostname, port)
        Promotion.redis = Redis(host=hostname, port=port, password=password)
        try:
            Promotion.redis.ping()
            Promotion.logger.info("Connection established")
        except ConnectionError:
            Promotion.logger.info(
                "Connection Error from: %s:%s", hostname, port)
            Promotion.redis = None
        return Promotion.redis

    @staticmethod
    def init_db(redis=None):
        """
        Initialized Redis database connection
        This method will work in the following conditions:
          1) In Bluemix with Redis bound through VCAP_SERVICES
          2) With Redis running on the local server as with Travis CI
          3) With Redis --link in a Docker container called 'redis'
          4) Passing in your own Redis connection object
        Exception:
        ----------
          DatabaseConnectionError - if ping() test fails
        """
        if redis:
            Promotion.logger.info("Using client connection...")
            Promotion.redis = redis
            try:
                Promotion.redis.ping()
                Promotion.logger.info("Connection established")
            except ConnectionError:
                Promotion.logger.error("Client Connection Error!")
                Promotion.redis = None
                raise DatabaseConnectionError(
                    'Could not connect to the clients Redis Service')
            return
        # Get the credentials from the Bluemix environment
        if 'VCAP_SERVICES' in os.environ:
            Promotion.logger.info("Using VCAP_SERVICES...")
            vcap_services = os.environ['VCAP_SERVICES']
            services = json.loads(vcap_services)
            creds = services['rediscloud'][0]['credentials']
            Promotion.logger.info("Conecting to Redis on host %s port %s",
                                  creds['hostname'], creds['port'])
            Promotion.connect_to_redis(creds['hostname'], creds[
                                       'port'], creds['password'])
        else:
            Promotion.logger.info(
                "VCAP_SERVICES not found, checking localhost for Redis")
            Promotion.connect_to_redis('127.0.0.1', 6379, None)
            if not Promotion.redis:
                Promotion.logger.info(
                    "No Redis on localhost, looking for redis host")
                Promotion.connect_to_redis('redis', 6379, None)
        if not Promotion.redis:
            # if you end up here, redis instance is down.
            Promotion.logger.fatal(
                '*** FATAL ERROR: Could not connect to the Redis Service')
            raise DatabaseConnectionError(
                'Could not connect to the Redis Service')
