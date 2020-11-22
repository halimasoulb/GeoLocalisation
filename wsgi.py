from app.py import Covid19Monitor

web_server = Covid19Monitor()

app = web_server.start()