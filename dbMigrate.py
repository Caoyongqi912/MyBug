# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午1:53
# @Author  : cyq
# @File    : dbMigrate.py

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from Model import models
from APP import create_app, db


app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
