import os

app_dir = os.path.dirname(__file__)
db_path = os.path.join(app_dir, '..', 'data', 'birthdays.db')
DATABASE = db_path
default_userid = '5c29d050-ce06-4741-bedb-ebaea573669a'