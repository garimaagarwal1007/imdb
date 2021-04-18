import os
from configparser import ConfigParser

config = ConfigParser()
config.read(os.path.join('cfg', 'config.ini'))


# class IMconfig:
#     __config = None
#
#     def __init__(self):
#         if not self.__config:
#             self.__config = ConfigParser()
#             file = 'config.ini'
#             self.__config.read(os.path.join('cfg', file))
#
#     @classmethod
#     def getInstance(cls):
#         if not cls.__config:
#             cls.__config = IMconfig()
#             return cls.__config.__config
#         else:
#             return cls.__config.__config
#
#     @staticmethod
#     def get(section, value):
#         conf = IMconfig.getInstance()
#         return conf.get(section, value)
#
#
# test = IMconfig()
# print(test)