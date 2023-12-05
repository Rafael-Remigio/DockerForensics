#!/usr/bin/python3

from flask import Flask, render_template
from src.http_util import HttpUtils


app = Flask(__name__)

base_url = 'http://localhost:2375'
http_utils = HttpUtils(base_url)

@app.route('/')
def index():

   images = http_utils.get_json_from_endpoint("images/json")

   containers = http_utils.get_json_from_endpoint("containers/json?all=true")

   return render_template("index.html",images=images,containers=containers)



@app.route('/container/<container_id>')
def inspect_container(container_id):

   # Fetch detailed data
   endpoint = "container/" + container_id + "/json" 
   data = http_utils.get_json_from_endpoint(endpoint)

   return render_template('container_inspection.html', container_data=data)

# main driver function
if __name__ == '__main__':

   # run() method of Flask class runs the application 
   # on the local development server.
   app.run()