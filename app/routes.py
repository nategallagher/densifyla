from flask import request, render_template, send_from_directory, redirect
from werkzeug.utils import secure_filename

from app import app, db
from app.models import Address

import os
import time


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        addr = Address(address=request.form['address'])
        filename = str(int(time.time() * 1000)) + "_" + secure_filename(addr.address)
        addr.report_folder = os.path.join(app.config['REPORT_FOLDER'], filename + ".pdf")
        addr.address_folder = os.path.join(app.config['ADDRESS_FOLDER'], filename + ".txt")

        txt_file = open(addr.address_folder, "w")
        txt_file.write(addr.address)
        txt_file.close()

        if app.config['DEBUG']:
            pdf_file = open(addr.report_folder, "w")
            pdf_file.write(addr.address)
            pdf_file.close()

        db.session.add(addr)
        db.session.commit()

    page = int(request.args.get('page', 1))
    page_object = Address().query.paginate(max_per_page=10, page=page)

    return render_template("index.html", page_object=page_object)


@app.route('/download/<file>')
def download(file):
    return send_from_directory(app.config['REPORT_FOLDER'], file)


@app.route('/delete/<address_id>')
def delete(address_id):
    addr = Address().query.filter_by(id=address_id).first()
    try:
        os.remove(addr.address_folder)
    except FileNotFoundError:
        pass
    try:
        os.remove(addr.report_folder)
    except FileNotFoundError:
        pass
    db.session.delete(addr)
    db.session.commit()
    return redirect('/')
