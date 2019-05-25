from flask import request, render_template, send_from_directory, redirect
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

    page = int(request.args.get('page', 1))
    page_object = Address().query.paginate(max_per_page=10, page=page)

    return render_template("index.html", page_object=page_object)


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['ADDRESS_FOLDER'], filename)


@app.route('/delete/<address_id>')
def delete(address_id):
    addr = Address().query.filter_by(id=address_id).first()
    os.remove(addr.address_folder)
    db.session.delete(addr)
    db.session.commit()
    return redirect('/')
