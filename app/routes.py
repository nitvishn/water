from app import app, db
from app.models import Community_table, Vendor_table
from flask import request
import json
from main import *

@app.route('/')
@app.route('/index')
def index():
    return "Water Tanker Routing API."

@app.route('/write')
def write_to_database():
    vendors = loadVendorsCSV('csvdata/vendors.csv')
    for vendor in vendors:
        db.session.add(Vendor_table(name=vendor.name, num_tankers=vendor.numTankers,tanker_capacity=vendor.tankerCapacity,latitude=vendor.x,longitude=vendor.y))

    communities = loadCommunitiesCSV('csvdata/communities.csv')
    for community in communities:
        db.session.add(Community_table(name=community.name, locality=community.locality, type=community.type, latitude=community.x, longitude=community.y, vendor_id = community.vendor_id))
    db.session.commit()

    return "Wrote " + str(len(vendors)) + " vendors and " + str(len(communities)) + " communities."

@app.route('/api')
def compute_route():
    date = request.args.get('date', default = "18-01-2019", type = str)
    vendor_id = request.args.get('vendor_id', default = 5, type = int)
    return json.dumps({'vendor_id': vendor_id, 'date': date})
