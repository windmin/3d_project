from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField,FloatField
from wtforms.validators import DataRequired,Regexp,EqualTo,Length,ValidationError,Email
from ..models import User, Role

class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('登录')


class CreateuserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'用户名只能是字母、数字、.、_')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    type = SelectField('User type',coerce=int,default=2)
    submit = SubmitField('Create')

    def __init__(self, *args, **kwargs):
        super(CreateuserForm, self).__init__(*args, **kwargs)
        self.type.choices = [(u.id,u.name) for u in Role.query.all()]


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email已存在！')


class EdituserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'用户名只能是字母、数字、.、_')])
    # password = PasswordField('密码', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    type = SelectField('User type',coerce=int,default=2)
    password = PasswordField('Change Password')
    status = BooleanField('Enable Account')
    submit = SubmitField('更新')
    def __init__(self, *args, **kwargs):
        super(EdituserForm, self).__init__(*args, **kwargs)
        self.type.choices = [(u.id,u.name) for u in Role.query.all()]


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    submit = SubmitField('Send')


class PasswordResetForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first() is None:
    #         raise ValidationError('Unknown email address.')