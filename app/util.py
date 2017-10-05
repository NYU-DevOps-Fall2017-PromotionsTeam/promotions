import logging
import sys

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def initialize_logging(log_level, flask_app):
    """ Initialized the default logging to STDOUT """
    if not flask_app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(flask_app.logger.handlers)
        for log_handler in handler_list:
            flask_app.logger.removeHandler(log_handler)
        flask_app.logger.addHandler(handler)
        flask_app.logger.setLevel(log_level)
        flask_app.logger.info('Logging handler established')
