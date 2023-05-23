import json
import psycopg2.extras

from flask import Flask, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

hostname = 'localhost'
database = 'todo-database'
username = 'postgres'
pwd = 'password'
port_id = 5432


def create_connection():
    connection = psycopg2.connect(host=hostname,
                                  dbname=database,
                                  user=username,
                                  password=pwd,
                                  port=port_id,
                                  )
    connection.autocommit = True

    return connection


@app.route('/table')
def index():
    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'select * from saved_notes'
    cur.execute(query)
    columns = list(cur.description)
    a = (cur.fetchall())
    results = []
    for row in a:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col.name] = row[i]
        results.append(row_dict)

    cur.close()
    connection.close()
    return results


@app.route('/add', methods=['POST'])
def add_activity():
    payload = request.json
    activity_data = payload["activity"]
    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'insert into saved_notes(activity) values(%s)'
    cur.execute(query, (activity_data,))
    cur.close()
    connection.close()
    return {'status': 'success'}


@app.route('/delete', methods=['POST'])
def delete_data():
    payload = request.json
    item = payload['item_number']
    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'delete from saved_notes where item_number=%s'
    cur.execute(query, (item,))
    cur.close()
    connection.close()
    return {'status': 'success'}


@app.route('/checkedTable')
def checked_table():
    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'select * from saved_notes where status=true'
    cur.execute(query)
    columns = list(cur.description)
    a = (cur.fetchall())
    results = []
    for row in a:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col.name] = row[i]
        results.append(row_dict)

    cur.close()
    connection.close()
    return results


@app.route('/edit', methods=['POST'])
def edit_data():
    payload = request.json
    item = payload['item_number']
    activity_item = payload['activity']

    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'update saved_notes set activity=%s where item_number=%s '
    cur.execute(query, (activity_item, item))
    cur.close()
    connection.close()
    return {'status': 'success'}


@app.route('/status', methods=['POST'])
def edit_status():
    payload = request.json
    item_value = payload['item_number']
    status = payload['status']
    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'update saved_notes set status=%s where item_number=%s '
    cur.execute(query, (status, item_value,))
    cur.close()
    connection.close()
    return {'status': 'success'}


if __name__ == "__main__":
    app.run(debug=True)
