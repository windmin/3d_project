#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Role, User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.main.filters import peixian_danyuan #自定义过滤器

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.jinja_env.filters['peixian_danyuan'] = peixian_danyuan #自定义过滤器
# app.jinja_env.filters['format_ten'] = format_ten #自定义过滤器
# app.jinja_env.filters['update_change_data'] = update_change_data #自定义过滤器

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()