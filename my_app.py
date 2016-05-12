from flask import Flask, render_template, session, redirect, request, url_for
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template

#for retrieving robot IPs
import urllib2
import json

#for parsing HTML retreived from robot_ips
from bs4 import BeautifulSoup


app = Flask(__name__)
Mobility(app)

app.secret_key = 'CHANGE_ME'

ip_url = "http://nixons-head.csres.utexas.edu:7979/hostsjson"
req = urllib2.Request(ip_url)
#response = urllib2.urlopen(req)
#result = response.read()
result = '{"bender":"101.101.101.101"}'
robot_ips = json.loads(result)

### ROUTING ###
@app.route('/')
@mobile_template('{mobile/}index.html')
def index(template):
	return render_template(template, robot_ips=robot_ips)

@app.route('/robot/<robot_name>')
@mobile_template('{mobile/}robot.html')
def robot(template, robot_name):
	if robot_name.lower() in robot_ips.keys():
		if ping_robot(robot_name):
			topics = get_topics(robot_name)
			return render_template(template, robot_name=robot_name, robot_ip=robot_ips[robot_name.lower()], topics=topics)
		else:
			return redirect(url_for('error'))
	else:
		return "no robot named " + robot_name

@app.route('/error')
@mobile_template('{mobile/}error.html')
def error(template):
	return render_template(template)


def ping_robot(robot):
	return True
	url = "http://" +  robot_ips[robot] + ":8080"
	req = urllib2.Request(ip_url)
	try:
		response = urllib2.urlopen(req, timeout=5)
	except urllib2.URLError:
		return False
	return True

def get_topics(robot):
	url = "http://" +  robot_ips[robot] + ":8080"
	req = urllib2.Request(ip_url)
	#response = urllib2.urlopen(req)
	#result = response.read()
	result = '<html><head><title>ROS Image Topic List</title></head><body><h1>Available ROS Image Topics:</h1><ul><li>/nav_kinect/rgb/<ul><li><a href="/stream_viewer?topic=/nav_kinect/rgb/image_color">image_color</a> (<a href="/snapshot?topic=/nav_kinect/rgb/image_color">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/rgb/image_rect_mono">image_rect_mono</a> (<a href="/snapshot?topic=/nav_kinect/rgb/image_rect_mono">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/rgb/image_raw">image_raw</a> (<a href="/snapshot?topic=/nav_kinect/rgb/image_raw">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/rgb/image_mono">image_mono</a> (<a href="/snapshot?topic=/nav_kinect/rgb/image_mono">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/rgb/image_rect_color">image_rect_color</a> (<a href="/snapshot?topic=/nav_kinect/rgb/image_rect_color">Snapshot</a>)</li></ul></li><li>/nav_kinect/depth_registered/<ul><li><a href="/stream_viewer?topic=/nav_kinect/depth_registered/sw_registered/image_rect">sw_registered/image_rect</a> (<a href="/snapshot?topic=/nav_kinect/depth_registered/sw_registered/image_rect">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/depth_registered/hw_registered/image_rect_raw">hw_registered/image_rect_raw</a> (<a href="/snapshot?topic=/nav_kinect/depth_registered/hw_registered/image_rect_raw">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/depth_registered/hw_registered/image_rect">hw_registered/image_rect</a> (<a href="/snapshot?topic=/nav_kinect/depth_registered/hw_registered/image_rect">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/depth_registered/image_raw">image_raw</a> (<a href="/snapshot?topic=/nav_kinect/depth_registered/image_raw">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/depth_registered/image">image</a> (<a href="/snapshot?topic=/nav_kinect/depth_registered/image">Snapshot</a>)</li><li><a href="/stream_viewer?topic=/nav_kinect/depth_registered/sw_registered/image_rect_raw">sw_registered/image_rect_raw</a> (<a href="/snapshot?topic=/nav_kinect/depth_registered/sw_registered/image_rect_raw">Snapshot</a>)</li></ul></li><li>/nav_kinect/projector/<ul></ul></li><li>/nav_kinect/depth/<ul><li><a href="/stream_viewer?topic=/nav_kinect/depth/image_raw">image_raw</a> (<a href="/snapshot?topic=/nav_kinect/depth/image_raw">Snapshot</a>)</li></ul></li><li>/nav_kinect/ir/<ul><li><a href="/stream_viewer?topic=/nav_kinect/ir/image_raw">image_raw</a> (<a href="/snapshot?topic=/nav_kinect/ir/image_raw">Snapshot</a>)</li></ul></li><li>/nav_kinect/depth_registered/sw_registered/<ul></ul></li></ul></body></html>'

	soup = BeautifulSoup(result, "html.parser")
	topics = set()
	for o in soup.findAll("ul"):
	    for l in o.findAll("li"):
	        for q in l:
	            if unicode(q).startswith("/"): #meaning its a topic name
	                pass
	            elif not "<ul>" in unicode(q) and not "(" in unicode(q) and not ")" in unicode(q): # a little hacky :/
	                if q["href"].startswith("/stream_viewer"):
	                    topics.add( q["href"].replace("/stream_viewer?topic=",""))
	    #r_topics.append("/".join(t.split("/")[2:]))
	return sorted(topics)



if __name__ == "__main__":
    app.run(debug=True)
