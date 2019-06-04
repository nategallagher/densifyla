from flask import request, render_template, send_from_directory, \
    redirect, flash, Markup
from flask_login import login_user, current_user
from werkzeug.utils import secure_filename

from app import app, db
from app.models import Address, User

import os


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    elif request.method == 'POST':
        addr = Address(address=request.form['address'])
        addr.report_folder = os.path.join(app.config['REPORT_FOLDER'], secure_filename(addr.address) + ".pdf")
        addr.address_folder = os.path.join(app.config['ADDRESS_FOLDER'], secure_filename(addr.address))

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            flash(Markup("Email address was not found. <a href=\"{{ url_for('register')}}\">Register?</a"))
        elif not user.check_password(password):
            flash("Password was incorrect. Forgot password?")
        else:
            login_user(user)
            return redirect('/')

    return render_template("login.html")


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
