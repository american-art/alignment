#!/usr/bin/env python
import logging

DIR_PATH = './../../aac-repos/'
REPOS = [
	# 'autry',
	'npg',
	'cbm',
	'wam',
	'nmwa',
]
IGNORE_DIRS = ['.git']
OUTPUT_DIR = 'output'

# tdb should set `tdb:unionDefaultGraph true`
FUSEKI_URL = 'http://localhost:3030'
GRAPH_BASE_URL = 'http://data.americanartcollaborative.org/'
# GRAPH_BASE_URL = 'http://data.aac.org/'
# FUSEKI_ACCOUNT = ('', '')
TDB_DATASET_NAME = 'american-art'
TDB_DEV_DATASET_NAME = 'american-art-dev'
FUSEKI_ACCOUNT = None
FUSEKI_FORCE_OVERWRITE = True # delete the data store which has the same name before import
LOG_LEVEL = logging.INFO
NETWORK_TIMEOUT = None