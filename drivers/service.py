from abc import ABCMeta, abstractmethod

class Service(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        '''Connects to the cloud service'''

    @abstractmethod
    def upload(self):
        '''Uploads the passed file to the service '''

    @abstractmethod
    def delete_old_files(self):
        '''Deletes old files from the service '''        