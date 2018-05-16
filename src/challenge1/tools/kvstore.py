
from abc import ABCMeta, abstractmethod

class KVStore(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key: str):
        """
        :param key: the key to look up
        :return: the value to post or None if not available
        """
        raise NotImplementedError()

    @abstractmethod
    def put(self, key: str, value: str):
        """
        :param key: the key to be added
        :param value: the value to be added
        :return: None
        """
        raise NotImplementedError()

class DictKVStore(KVStore):
    def __init__(self):
        self.store = dict()

    def get(self, key):
        """
        :param key: the key to look up
        :return: the value to post
        """
        return self.store.get(key, None)

    def put(self, key: str, value: str):
        """
        :param key: the key to be added
        :param value: the value to be added
        :return: None
        """
        if self.get(key):
            raise Exception("Key Already Exsists")
        self.store[key] = value