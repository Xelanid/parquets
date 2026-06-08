import datetime
from typing import Any
from dataclasses import dataclass


@dataclass
class ConnectionSchema:
	connectionId : int
	engine       : str
	host         : str
	port         : int
	databaseName : str
	username     : str
	password     : str
	createdAt    : datetime


	@staticmethod
	def from_dict(obj:Any)->'ConnectionSchema':
		assert isinstance(obj, dict)
		connectionId = obj.get("connection_id")
		engine       = obj.get("engine")
		host         = obj.get("host")
		port         = obj.get("port")
		databaseName = obj.get("database_name")
		username     = obj.get("username")
		password     = obj.get("password")
		createdAt    = obj.get("created_at")
		return ConnectionSchema(connectionId, engine, host, port, databaseName, username, password, createdAt)