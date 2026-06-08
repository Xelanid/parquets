import configparser
import pathlib
from collections import namedtuple

class Config:
	def __init__(self, in_dict:dict):
		assert isinstance(in_dict, dict)
		for key, val in in_dict.items():
			if isinstance(val, (list, tuple)):
				setattr(self, key, [Config(x) if isinstance(x, dict) else x for x in val])
			else:
				setattr(self, key, Config(val) if isinstance(val, dict) else val)

def to_namedtuple(dict_data):
	
    return namedtuple(
        "Config", dict_data.keys()
    )(*tuple(map(lambda x: x if not isinstance(x, dict) else to_namedtuple(x), dict_data.values())))

def config_from_init():
	absolute = pathlib.Path(__file__).parent.absolute()
	real_path = '{}/config.ini'.format(absolute)
	config = configparser.ConfigParser()
	config.read(real_path)
	dictionary = {}
	for ss in config.sections():
		items = dict(config.items(ss))
		ss = ss.lower().replace('-','_')
		dictionary[ss] = items	
	obj = Config(dictionary)
	
	return 	obj

	
		

