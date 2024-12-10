#! /usr/bin/env python3

from application import APP
from application import DB_HANDLE


if __name__ == '__main__':
    DB_HANDLE.connect_to_database()
    APP.run(host='0.0.0.0', port=2137, debug=True)
