from app import app, db
from app.models import Community_table, Vendor_table

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Community_table': Community_table, 'Vendor_table': Vendor_table}
