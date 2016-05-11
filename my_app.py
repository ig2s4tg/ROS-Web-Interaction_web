from flask import Flask, render_template, session, redirect, request, url_for
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template

import urllib2
import json

app = Flask(__name__)
Mobility(app)

app.secret_key = 'CHANGE_ME'

ip_url = "http://nixons-head.csres.utexas.edu:7979/hostsjson"
req = urllib2.Request(ip_url)
response = urllib2.urlopen(req)
result = response.read()
robot_ips = json.loads(result)

### ROUTING ###
@app.route('/')
@mobile_template('{mobile/}index.html')
def index(template):
	return render_template(template, robot_ips=robot_ips)

@app.route('/robot/<robot_name>')
@mobile_template('{mobile/}robot.html')
def robot(template, robot_name):
	#no switch in python :'(
	if robot_name.lower() in robot_ips.keys():
		return render_template(template, robot_name=robot_name, robot_ip=robot_ips[robot_name.lower()])
	else:
		return "no robot named " + robot_name


if __name__ == "__main__":
    app.run(debug=True)
