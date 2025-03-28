from abc import ABCMeta, abstractmethod
import gzip
import os
import sys
import errno


class Database(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        '''Connects to the database tool'''
        
    @abstractmethod
    def dump(self):
        '''load the database contents to the  filename'''

    def _compress(self, file_name):
        '''
        Compress the passed file into a zip


        '''

        self.logger.info("Compressing  file...")
        try:
            sql_file = open(file_name, 'rb')
        except IOError:
            self.logger.critical("No such file or directory %s" % (file_name))
            sys.exit(errno.ENOENT)

        try:
            gz_file_name = file_name + '.gz'
            gz_file      = gzip.open(gz_file_name, 'wb')
            gz_file.writelines(sql_file)
        except IOError:
            self.logger.critical("Couldn't write file %s" % (gz_file_name))
            sys.exit(errno.ENOENT)

        sql_file.close()
        gz_file.close()

        os.unlink(file_name)
        return gz_file_name