# coding: utf-8
"""
project management
 -- database management
    -- python manage.py db init: create migrations folder
    -- python manage.py db migrate: database migrate
    -- python manage.py db upgrate: upgrade database
    -- python manage.py shell
       >> Role.insert_roles() : create user roles

 -- add administrator
    -- python manage.py admin
       \_admin username:
       \_admin email:
       \_admin password:

 -- add users
    -- python manage.py adduser
       \_username:
       \_password:
       \_email:
       \_[1:moderator 2:admin 3:user]:

 -- run project
    -- python manage.py runserver

 -- shell environment
    -- python manage.py shell

 -- run your unit tests
    -- python manage.py test

"""

import sys
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from auth import db, app
from auth.models import User , Role

# 编码设置
reload(sys)
sys.setdefaultencoding('utf-8')


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """自动加载环境"""
    return dict(
        app = app,
        db = db,
        User = User,
        Role = Role
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """run your unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def admin():
    """add administrator"""
    from getpass import getpass
    username = raw_input("\_admin username: ")
    email = raw_input("\_admin email: ")
    password = getpass("\_admin password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = 2
    )
    db.session.add(u)
    db.session.commit()
    print "<admin user %s add in database>" % username


@manager.command
def adduser():
    """add user"""
    from getpass import getpass
    username = raw_input("\_username: ")
    email = raw_input("\_email: ")
    role_id = raw_input("\_[1:moderator 2:admin 3:user]: ")
    password = getpass("\_password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = role_id
    )
    db.session.add(u)
    db.session.commit()
    print "<user %s add in database>" % username

@manager.command
def insert_roles():
    """
    insert all Roles in command line
    -------------------------------
    User: write & comment
    Moderator: write & comment & moderate_comments
    Administrator: full permissions
    """
    roles = {
        'User': (Permission.COMMENT | Permission.WRITE_ARTICLES, True),
        'Moderator': (Permission.COMMENT |
                      Permission.WRITE_ARTICLES |
                      Permission.MODERATE_COMMENTS, False),
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
    print('roles has been inserted!')
    sys.exit(0)


@manager.command
def test() :
    import unittest
    tests = unittest.TestLoader().discover('tests')
    ret = not  unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()
    sys.exit(ret)

if __name__ == '__main__':
    manager.run()

