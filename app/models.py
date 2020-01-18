from app import db

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    locality = db.Column(db.String(120))
    name = db.Column(db.String(200))
    type = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'),
                          nullable=False)


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    num_tankers = db.Column(db.Integer)
    tanker_capacity = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    communities = db.relationship('Community', backref='vendor', lazy=True)
