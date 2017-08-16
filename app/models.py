from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for


class Permission:
    # FOLLOW = 0x01
    # COMMENT = 0x02
    # WRITE_ARTICLES = 0x04
    # MODERATE_COMMENTS = 0x08
    # ADMINISTER = 0x80
    # 8 | 7 | 6 | 5 | 4  |   3    |   2    |    1
    # ADMINISTER | | | | | EXPORT | IMPORT | READ |
    READ = 0x01 #查看本人数据权限
    IMPORT = 0x02 #导入、添加
    EXPORT = 0x04 #导出
    ADMINISTER =0x80 #管理员权限


#SQLite define Table
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    #2表关系
    # users = db.relationship('User', backref='role')
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.READ | \
                     Permission.IMPORT | \
                     Permission.EXPORT, True), \
            # 'Moderator': (Permission.READ | \
            # Permission.IMPORT | \
            # Permission.EXPORT | \
            # Permission.ADMINISTER, False), \
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) #外键role_id = roles.id= roles表中的id
    rate = db.Column(db.Float)
    status = db.Column(db.Boolean, default=True)
    group = db.Column(db.String(16))
    code = db.Column(db.String(3))
    gerenliushuihao = db.Column(db.Integer, default=0)
    sid = db.Column(db.String(256))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            # if self.email == current_app.config['FLASKY_ADMIN']:
            if self.username == 'admin':
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password2(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        # self.password = new_password
        # db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

    # JSON
    def to_json(self):
        json_userinfo = {
            'username': self.username,
            'role': self.role,
            # 'author': url_for('api.get_user', id=self.author_id, _external=True),
        }
        return json_userinfo

    # @staticmethod
    # def from_json(json_userinfo):
    #     username = json_userinfo.get('username')
    #     if username is None or username == '':
    #         raise ValidationError('comment does not have a body')
    #     return User(username=username)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 设备表
class ShebeiTable(db.Model):
    __tablename__ = '设备'
    id = db.Column(db.Integer, primary_key=True)
    shebei_name = db.Column(db.String(64))
    front_slotNums = db.Column(db.Integer) #slot块数
    front_slot_rows = db.Column(db.Integer) #每块slot有几排
    front_slot_cols = db.Column(db.Integer) #每块slot有几列
    back_slotNums = db.Column(db.Integer)
    back_slot_rows = db.Column(db.Integer)
    back_slot_cols = db.Column(db.Integer)
    slot_used_list = db.Column(db.String()) #已被占用的端口 例：[1(1,4),3(2,3),4(3,1),7(3,24)]
    def __repr__(self):
        return '<设备 %r>' % self.id