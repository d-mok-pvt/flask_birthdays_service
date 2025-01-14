import os

URL = 'http://app:5001'
BIRTHDAYS_API_URL = URL + '/api/birthdays'
USERS_API_URL = URL + '/api/internal/admin/users'
SWAGGER_UI_URL = URL + '/swagger'
SWAGGER_JSON_URL = URL + '/static/swagger.json'

# DATABASE = "birthdays.db"
app_dir = os.path.dirname(__file__)
print(app_dir)
db_path = os.path.join(app_dir, '..', 'data', 'birthdays.db')
DATABASE = db_path
