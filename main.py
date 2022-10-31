from os import environ as env
from configparser import ConfigParser as cp
import ramfac

config = cp()
config.read('env/config.cfg')
for key in config['azure']:
    env[key] = config['azure'][key]

c = ramfac.customer('35544712-2af9-4a99-be71-9da4a6eb9ab0')
u = ramfac.uniqueList(c.getDevices(), 'userId')