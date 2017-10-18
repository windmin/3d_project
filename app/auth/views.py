from flask import render_template, redirect, request, url_for, flash, session
from . import auth
from .forms import LoginForm, CreateuserForm, EdituserForm, PasswordResetForm, PasswordResetRequestForm
from ..models import User

from .. import db
from flask_login import login_user,login_required,logout_user,current_user
from ..decorators import admin_required
# from ..email import send_email


from urllib.request import urlopen,Request
from urllib.error import HTTPError


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, status=True).first()
        if user is None:
            flash('Your accout is disabled. Please contact administrator.')
        elif user is not None and user.verify_password(form.password.data):
            login_user(user)

            user.sid = session['_id']
            db.session.add(user)
            db.session.commit()

            return redirect(request.args.get('next') or url_for('main.manage_jumping'))
        else:
            flash('Invalid username or password.')
    return render_template('auth/login.html', form=form) #templates/auth/login.html


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/account', methods=['GET', 'POST'])
@login_required
@admin_required
def account():
    if current_user.status == False:
        return redirect(url_for('auth.login'))
    # #判断是否有新登入
    # user_result = User.query.filter_by(username=current_user.username).first()
    # if user_result.sid != session['_id']:
    #     del_account_id = session['_id']
    # else:
    #     del_account_id = ''
    # #判断是否有新登入
    form = CreateuserForm()
    accounts = User.query.all()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        type = form.type.data
        if username != '' and password != '' and email != '' and type != '' :
            if User.query.filter_by(username=username).first():
                flash(username+'已注册！请更换username重新注册！')
            else:
                db.session.add(User(username = username, \
                                   password = password, \
                                   email = email, \
                                   role_id = type))
                db.session.commit()
                return redirect(url_for('auth.account'))
    return render_template('auth/account.html',accounts=accounts,form=form)


@auth.route('/account/delete/<id>',methods=['GET','POST'])
@login_required
@admin_required
def account_delete(id):
    if current_user.status == False:
        return redirect(url_for('auth.login'))
    result = User.query.filter_by(id=id).first()
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('auth.account'))


@auth.route('/account/edit/<id>',methods=['GET','POST'])
@login_required
@admin_required
def account_edit(id):
    if current_user.status == False:
        return redirect(url_for('auth.login'))
    # #判断是否有新登入
    # user_result = User.query.filter_by(username=current_user.username).first()
    # if user_result.sid != session['_id']:
    #     del_account_id = session['_id']
    # else:
    #     del_account_id = ''
    # #判断是否有新登入
    result = User.query.filter_by(id=id).first()
    form = EdituserForm()
    if form.validate_on_submit():
        result.username = form.username.data
        if form.password.data != '':
            result.password = form.password.data
        result.email = form.email.data
        result.role_id = form.type.data
        result.status = form.status.data

        db.session.add(result)
        db.session.commit()
        return redirect(url_for('auth.account'))
    form.username.data = result.username
    # form.password.data = ''
    form.email.data = result.email
    form.type.data = result.role_id
    form.status.data = result.status
    return render_template('auth/account-edit.html',form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.baojialiebiao'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))

            flash('An email with instructions to reset your password has been sent to you.')
        else:
            flash('该邮箱没有注册记录')
            return redirect(url_for('auth.password_reset_request'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>/<email>', methods=['GET', 'POST'])
def password_reset(token,email):
    # if not current_user.is_anonymous:
    #     return redirect(url_for('main.baojialiebiao'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('该邮箱没有注册记录')
            return redirect(url_for('auth.login'))
        if user.reset_password2(token):
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash(user.username + ', Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.baojialiebiao'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/lock')
def lock():
    return render_template('auth/lock.html')