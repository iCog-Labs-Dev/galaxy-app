#!/home/hope/New_Galaxy/galaxy_app_test/venv/bin/python3

"""
Read a file from stdin, split each line and write fields one per line to
stdout.

TODO: is this really that useful?
"""

import sys

for line in sys.stdin:
    for field in line.split():
        print(field)
