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
        db.session.add(Vendor_table(name=vendor.name, num_tankers=vendor.numTankers,
                                    tanker_capacity=vendor.tankerCapacity, latitude=vendor.x, longitude=vendor.y))

    communities = loadCommunitiesCSV('csvdata/communities.csv')
    for community in communities:
        db.session.add(Community_table(name=community.name, locality=community.locality, type=community.type,
                                       latitude=community.x, longitude=community.y, vendor_id=community.vendor_id))
    db.session.commit()

    return "Wrote " + str(len(vendors)) + " vendors and " + str(len(communities)) + " communities."


@app.route('/api')
def compute_route():
    date = datetime.datetime.strptime(request.args.get('date', default="18-01-2019", type=str), "%d-%m-%Y")
    vendor_id = request.args.get('vendor_id', default=1, type=int)
    vendors = loadVendors()
    communities = loadCommunities()
    res = get_res('csvdata/austin_water.csv')
    for community in communities:
        community.assign_function(res)
        for vendor in vendors:
            if community.vendor_id == vendor.id:
                vendor.communities.append(community)

    for vendor in vendors:
        if vendor.id == vendor_id:
            print(tsp(vendor, date))
            return json.dumps(tsp(vendor, date))
    return json.dumps({'vendor_id': vendor_id, 'date': date})
