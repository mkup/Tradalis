import configparser

from env.Env import Env

#  read configuration file
conf = configparser.RawConfigParser()
conf.read('tradalis.conf')

e = Env(conf)
e.stop()