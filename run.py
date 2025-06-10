#coding=utf-8
"""
# Author: Wenbing.Wang
# Created Time : 二  6/10 08:14:54 2025

# File Name: run.py
# Description:

"""

from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=9999, debug=True)
