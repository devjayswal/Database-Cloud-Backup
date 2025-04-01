from importlib import import_module
import sys
import logging
import errno

class Factory:
    def __init__(self):
        self.logger = logging.getLogger('clouddump')

    def create(self, driver_name, params):
        class_name = 'Driver' + driver_name.capitalize()
        try:
            module = import_module(f'drivers.driver_{driver_name}')
            klass = getattr(module, class_name)
        except ModuleNotFoundError:
            self.logger.critical(f"Module 'drivers.driver_{driver_name}' not found.")
            sys.exit(errno.ENOENT)  # Exit with 'No such file or directory' error code
        except AttributeError:
            self.logger.critical(f"Class {class_name} not found in module 'drivers.driver_{driver_name}'.")
            sys.exit(errno.EINVAL)  # Exit with 'Invalid argument' error code
        except Exception as e:
            self.logger.critical(f"Unexpected error while creating {class_name}: {e}")
            sys.exit(1)  # Generic failure

        return klass(params)
