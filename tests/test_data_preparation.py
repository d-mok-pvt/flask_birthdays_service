import logging
import sqlite3

import pytest

from tests.test_config import DATABASE
from tests.test_utils import generate_name, generate_date, generate_uuid


def generate_records(num_records, userid):
    records = ()
    for i in range(num_records):
        record = {
            'uuid': generate_uuid(),
            'name': generate_name() + "-Test",
            'date': generate_date(),
            'userid': userid
        }
        records += (record,)
    return records


@pytest.fixture(scope="session", autouse=True)
def prepare_database(setup_user_1):
    records = generate_records(10, setup_user_1.userid)
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    logging.info(f"Preparing database with records {records}")
    for record in records:
        cursor.execute("INSERT INTO birthdays (uuid, name, date, userid) VALUES (?, ?, ?, ?)",
                       (record['uuid'], record['name'], record['date'], record['userid']))
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
