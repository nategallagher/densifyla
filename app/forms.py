from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    email = StringField(validators=[Email(), DataRequired(), Length(min=3, max=25)])
    password = PasswordField(validators=[Length(min=8, max=32), DataRequired()])


class RegisterForm(FlaskForm):
    register_email = StringField(validators=[Email(), DataRequired(), Length(min=3, max=25)])
    register_password = PasswordField(validators=[Length(min=8, max=32), DataRequired()])
    register_password_2 = PasswordField(validators=[Length(min=8, max=32), DataRequired()])

    def validate_register_password_2(self, register_password_2):
        if self.register_password.data != register_password_2.data:
            raise ValidationError("Passwords were not equal. Registration failed. Please try again.")


class ForgotPasswordForm(FlaskForm):
    forgot_password_email = StringField(validators=[Email(), DataRequired(), Length(min=3, max=25)])
