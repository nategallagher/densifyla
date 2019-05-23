from flask import request, render_template
from werkzeug.utils import secure_filename

from app import app, db
from app.models import Address

import os


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        addr = Address(address=request.form['address'])
        addr.report_folder = os.path.join(app.config['REPORT_FOLDER'], secure_filename(addr.address))
        addr.address_folder = os.path.join(app.config['ADDRESS_FOLDER'], secure_filename(addr.address))

        txt_file = open(addr.address_folder, "w")
        txt_file.write(addr.address)
        txt_file.close()

        db.session.add(addr)
        db.session.commit()

    page_object = Address().query.paginate(max_per_page=10)

    return render_template("index.html", items=page_object.items)


@app.route('/report')
def report():
    """
    API route for feasability report.

    Returns:
        feasibility report pdf
    """
    address = request.args.get('address', None)
    # store address
    # once grasshopper processes code
    #
    return "The address requested was: {}".format(address)
