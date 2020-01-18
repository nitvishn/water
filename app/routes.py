from app import app
from flask import request
import json

@app.route('/')
@app.route('/index')
def index():
    return "Water Tanker Routing API."

@app.route('/api/')
def compute_route():
    date = request.args.get('date', default = "18-01-2019", type = str)
    vendor_id = request.args.get('vendor_id', default = 5, type = int)
    return json.dumps({'vendor_id': vendor_id, 'date': date})
