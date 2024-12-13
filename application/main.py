#! /usr/bin/env python3

from application import APP
from application import DB_HANDLE

DB_HANDLE.connect_to_database()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=2137, debug=True)
