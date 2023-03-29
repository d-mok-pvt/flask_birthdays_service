import os

FRONT_URL = 'http://app:5000'
API_URL = FRONT_URL + '/api/birthdays'
SWAGGER_UI_URL = FRONT_URL + '/swagger'
SWAGGER_JSON_URL = FRONT_URL + '/static/swagger.json'

# DATABASE = "birthdays.db"
app_dir = os.path.dirname(__file__)
db_path = os.path.join(app_dir, '..', 'data', 'birthdays.db')
DATABASE = db_path
