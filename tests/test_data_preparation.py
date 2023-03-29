import pytest
import sqlite3
from tests.test_config import DATABASE
from tests.test_utils import generate_name, generate_date, generate_uuid


def generate_records(num_records):
    records = ()
    for i in range(num_records):
        record = {
            'uuid': generate_uuid(),
            'name': generate_name() + "-Test",
            'date': generate_date()
        }
        records += (record,)
    return records


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    records = generate_records(10)
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    for record in records:
        cursor.execute("INSERT INTO birthdays (uuid, name, date ) VALUES (?, ?, ?)",
                       (record['uuid'], record['name'], record['date']))
    db_connection.commit()
    cursor.close()

    yield

    cursor = db_connection.cursor()
    for record in records:
        cursor.execute("DELETE FROM birthdays WHERE uuid = ?",
                       (record['uuid'],))
    db_connection.commit()
    cursor.close()
    db_connection.close()
