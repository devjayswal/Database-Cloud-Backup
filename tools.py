import json
import sys
import logging
import logging.handlers

def introduction():
    '''Prints starting message'''

    print("""
    Welcome to This project!

    This is a tool to help you to make backup of your database.

    """)

def load_config():

    try:
        introduction()
        print("Loading configuration...")
        json_data = open('config.json')
        config    = json.load(json_data)
        json_data.close()
        return config
    except Exception:
        print("""No configuration file found. Please create a config.json file with the following format:""")
        sys.exit(1)

def init_logger(file_name='clouddump.log'):
    logger = logging.getLogger('clouddump')
    log_file_handler = logging.handlers.RotatingFileHandler(
        file_name, maxBytes = 10**9)
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file_handler.setFormatter(log_format)
    logger.addHandler(log_file_handler)
    logger.setLevel(logging.DEBUG)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v' or sys.argv[1] == '--verbose':
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            logger.addHandler(console)