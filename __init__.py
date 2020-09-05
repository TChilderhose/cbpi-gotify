from modules import app, cbpi
from thread import start_new_thread
import logging
import time
import requests

gotify_token = None
gotify_url = None
gotify = None

def gotifyToken():
	global gotify_token
	gotify_token = cbpi.get_config_parameter("gotify_token", None)
	if gotify_token is None:
		print "INIT gotify Token"
		try:
			cbpi.add_config_parameter("gotify_token", "", "text", "gotify API Token")
		except:
			cbpi.notify("gotify Error", "Unable to update database. Update CraftBeerPi and reboot.", type="danger", timeout=None)

def gotifyUrl():
	global gotify_user
	gotify_url = cbpi.get_config_parameter("gotify_url", None)
	if gotify_url is None:
		print "INIT gotify User Key"
		try:
			cbpi.add_config_parameter("gotify_url", "", "text", "gotify URL")
		except:
			cbpi.notify("gotify Error", "Unable to update database. Update CraftBeerPi and reboot.", type="danger", timeout=None)

@cbpi.initalizer(order=9000)
def init(cbpi):
	global gotify
	cbpi.app.logger.info("INITIALIZE Gotify PLUGIN")
	gotifyUrl()
	gotifyToken()
	if gotify_token is None or not gotify_token:
		cbpi.notify("gotify Error", "Check gotify API Token is set", type="danger", timeout=None)
	elif gotify_url is None or not gotify_url:
		cbpi.notify("gotify Error", "Check gotify URL is set", type="danger", timeout=None)
	else:
		gotify = "OK"

@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
	gotifyData = {}
	gotifyData["message"] = message["message"]
	gotifyData["title"] = message["headline"]
	requests.post(gotify_url.strip("/") + "/message?token=" + gotify_token, data=gotifyData)
