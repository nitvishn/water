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
        db.session.add(Vendor_table(name=vendor.name, num_tankers=float(vendor.numTankers),
                                    tanker_capacity=float(vendor.tankerCapacity), latitude=float(vendor.x), longitude=float(vendor.y)))

    communities = loadCommunitiesCSV('csvdata/communities.csv')
    for community in communities:
        if community.type == 'Apartment':
            persons = random.randrange(100, 200)
        elif community.type == 'House':
            persons = random.randrange(2, 6)
        elif community.type == 'Restaurant':
            persons = random.randrange(20, 30)
        db.session.add(Community_table(name=community.name, locality=community.locality, type=community.type,
                                       latitude=float(community.x), longitude=float(community.y), vendor_id=int(community.vendor_id), num_persons = int(persons)))
    db.session.commit()

    return "Wrote " + str(len(vendors)) + " vendors and " + str(len(communities)) + " communities."

@app.route('/delete')
def delete_all_entries():
    c_count = 0
    for c in Community_table.query.all():
        db.session.delete(c)
        c_count += 1
    v_count = 0
    # for v in Vendor_table.query.all():
    #     db.session.delete(v)
    #     v_count += 1
    # db.session.commit()
    return "Deleted " + str(v_count) + " vendors and " + str(c_count) + " communities."

@app.route('/api')
def compute_route():
    vendors = loadVendors()
    communities = loadCommunities()
    date = datetime.datetime.strptime(request.args.get('date', default="18-01-2019", type=str), "%d-%m-%Y")
    vendor_id = request.args.get('vendor_id', default=1, type=int)
    res = get_res('csvdata/austin_water.csv')

    for community in communities:
        community.assign_function(res)
        for vendor in vendors:
            if community.vendor_id == vendor.id:
                vendor.communities.append(community)

    vendor = vendors[0]
    return json.dumps(tsp(vendor, date))
    # for vendor in vendors:
    #     if vendor.id == vendor_id:
    #         print(tsp(vendor, date))
    #         return json.dumps(tsp(vendor, date))
    # return json.dumps({'vendor_id': vendor_id, 'date': str(date)})
