from flask import request, render_template, send_from_directory, \
    redirect, flash, Markup, url_for, abort
from flask_login import login_user, current_user, logout_user
from flask_mail import Message
from werkzeug.utils import secure_filename

from app import app, db
from app.models import Address, User
from app.forms import LoginForm, ForgotPasswordForm, RegisterForm, ResetPasswordForm
from app.email import send_mail_thread

import os


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    elif request.method == 'GET':
        pass
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
        login_form = LoginForm()
        if not login_form.validate_on_submit():
            for field_name, error_msg in login_form.errors.items():
                flash("{}: {}".format(field_name, error_msg), "error")
        else:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if not user:
                flash(Markup("Email address was not found. <a href=\"{{ url_for('register')}}\" "
                             "data-toggle=\"modal\" data-target=\"#registerModal\">Register?</a"), "error")
            elif not user.check_password(password):
                flash("Password was incorrect. Forgot password?")
            else:
                login_user(user)
                return redirect('/')

    return render_template("login.html", login_form=LoginForm(), forgot_password_form=ForgotPasswordForm(),
                           register_form=RegisterForm())


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


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        register_form = RegisterForm()
        if not register_form.validate_on_submit():
            for field_name, error_msg in register_form.errors.items():
                flash("{}: {}".format(field_name, error_msg), "error")
        else:
            new_user = User()
            new_user.email = request.form['register_email']
            new_user.set_password(request.form['register_password'])
            db.session.add(new_user)
            db.session.commit()
            flash("You have successfully registered an account with DensifyLA! "
                  "An email confirmation has been sent to {}".format(new_user.email), "message")
            msg = Message('Welcome to DensifyLA',
                          sender='noreply@densifyla.com',
                          recipients=[new_user.email])
            token = new_user.get_email_confirmation_token()
            msg.body = render_template("email/email_confirmation.txt",
                                       email_confirmation_link=url_for('confirm_email', token=token))
            msg.html = render_template("email/email_confirmation.html",
                                       email_confirmation_link=url_for('confirm_email', token=token))
            send_mail_thread(app, msg)

    return redirect('/')


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    if request.method == 'POST':
        forgot_password_form = ForgotPasswordForm()
        if not forgot_password_form.validate_on_submit():
            for field_name, error_msg in forgot_password_form.errors.items():
                flash("{}: {}".format(field_name, error_msg), "error")
        else:
            email = request.form['forgot_password_email']
            user = User.query.filter_by(email=email).first()
            if user:
                token = user.get_password_reset_token()
                msg = Message('Reset your password',
                              sender='noreply@densifyla.com',
                              recipients=[user.email])
                msg.body = render_template("email/forgot_password.txt",
                                           reset_password_link=url_for('reset_password', token=token))
                msg.html = render_template("email/forgot_password.html",
                                           reset_password_link=url_for('reset_password', token=token))
                send_mail_thread(app, msg)
                flash("A password reset link has been sent to {}".format(email))
            # todo: password reset  logic
    return redirect('/')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect('/')
    user = User.verify_password_reset_token(token)
    if not user:
        return abort(401)
    if request.method == 'GET':
        return render_template("reset_password.html", reset_password_form=ResetPasswordForm(), token=token)
    elif request.method == 'POST':
        reset_password_form = ResetPasswordForm()
        if not reset_password_form.validate_on_submit():
            for field_name, error_msg in reset_password_form.errors.items():
                flash("{}: {}".format(field_name, error_msg), "error")
                return render_template("reset_password.html", reset_password_form=ResetPasswordForm(), token=token)
        else:
            user.set_password(reset_password_form.reset_password.data)
            db.session.commit()
            flash("You have successfully reset your password.")
            msg = Message('Your password has been reset',
                          sender='noreply@densifyla.com',
                          recipients=[user.email])
            msg.body = render_template("email/password_reset_confirmation.txt")
            msg.html = render_template("email/password_reset_confirmation.html")
            send_mail_thread(app, msg)
            return redirect('/')


@app.route('/confirm-email/<token>')
def confirm_email(token):
    user = User.verify_email_confirmation_token(token)
    if not user:
        return abort(401)
    user.email_confirmed = True
    db.session.commit()
    flash("Thank you! Your email has been confirmed.")
    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
