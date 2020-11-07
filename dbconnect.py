import pymysql

def connection():
	conn = pymysql.connect( host = "localhost",
		user ="root",
		passwd = "password",
		db = "recensement"
		)
	c = conn.cursor()
	return c, conn