from app import db

class Vendor_table(db.Model):
    __tablename__ = "vendor_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    num_tankers = db.Column(db.Integer)
    tanker_capacity = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # communities = db.relationship('Community_table', backref='vendor', lazy=True)

class Community_table(db.Model):
    __tablename__ = "community_table"
    id = db.Column(db.Integer, primary_key=True)
    locality = db.Column(db.String(120))
    name = db.Column(db.String(200))
    type = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # vendor_id = db.Column(db.Integer, db.ForeignKey('vendor_table.id'))
    vendor_id = db.Column(db.Integer)
    num_persons = db.Column(db.Integer)
