from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    email = StringField(validators=[Email(), DataRequired(), Length(min=3, max=140)])
    password = PasswordField(validators=[Length(min=8, max=128), DataRequired()])


class RegisterForm(FlaskForm):
    register_email = StringField(validators=[Email(), DataRequired(), Length(min=3, max=140)])
    register_password = PasswordField(validators=[Length(min=8, max=128), DataRequired()])
    register_password_2 = PasswordField(validators=[Length(min=8, max=128), DataRequired()])

    def validate_register_password_2(self, register_password_2):
        if self.register_password.data != register_password_2.data:
            raise ValidationError("Passwords were not equal. Registration failed. Please try again.")


class ForgotPasswordForm(FlaskForm):
    forgot_password_email = StringField(validators=[Email(), DataRequired(), Length(min=3, max=140)])


class ResetPasswordForm(FlaskForm):
    reset_password = PasswordField(validators=[Length(min=8, max=128), DataRequired()])
    reset_password_2 = PasswordField(validators=[Length(min=8, max=128), DataRequired()])

    def validate_reset_password_2(self, reset_password_2):
        if self.reset_password.data != reset_password_2.data:
            raise ValidationError("Passwords were not equal. Password reset failed. Please try again.")
