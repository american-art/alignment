#!/usr/bin/env python

from pyspark import SparkContext, StorageLevel
from pyspark.sql.functions import explode
from py4j.java_gateway import java_import
from digWorkflow.workflow import Workflow
from digSparkUtil.fileUtil import FileUtil

import json
import sys, os
import logging
import urlparse, urllib
import shutil
import time
import zipfile
from importlib import import_module

import csv
import json
import codecs
import subprocess

logging.basicConfig(
    stream = sys.stdout,
    format = '%(asctime)s [%(levelname)s] %(message)s',
    datefmt = '%d %b %Y %H:%M:%S'
)

def init_repo_config(config):
    # fill variables
    name = config['name']
    if 'input_file' not in config:
        config['input_file'] = name + '.csv'
    if 'input_file_type' not in config:
        config['input_file_type'] = 'csv'
    if 'output_dir' not in config:
        config['output_dir'] = 'output'
    if 'output_file_name' not in config:
        config['output_file_name'] = name
    if 'output_file_type' not in config:
        config['output_file_type'] = 'n3'
    if 'model_file' not in config:
        config['model_file'] = name + '-model.ttl'
    if 'num_partitions' not in config:
        config['num_partitions'] = 1
    if 'csv_to_jl' not in config:
        config['csv_to_jl'] = False
    if 'preprocess' not in config:
        config['preprocess'] = None
    if 'additional_settings' not in config:
        config['additional_settings'] = {}

    # add settings
    if config['input_file_type'] == 'csv' and 'karma.input.delimiter' not in config['additional_settings']:
        config['additional_settings']['karma.input.delimiter'] = ','
    if config['output_file_type'] == 'n3' and 'karma.output.format' not in config['additional_settings']:
        config['additional_settings']['karma.output.format'] = 'n3'

    # construct path
    abs_path = os.path.abspath(config['path'])
    abs_path = os.path.join(abs_path, config['name'])
    config['input_file'] = os.path.join(abs_path, config['input_file'])
    config['output_dir'] = os.path.join(abs_path, config['output_dir'])
    config['output_file'] = os.path.join(abs_path, config['output_file_name'] + '.' + config['output_file_type'])
    config['model_file'] = os.path.join(abs_path, config['model_file'])
    if config['preprocess']:
        config['preprocess'][0] = os.path.join(abs_path, config['preprocess'][0])
        config['preprocess'][1] = os.path.join(abs_path, config['preprocess'][1])
        config['preprocess'][2] = os.path.join(abs_path, config['preprocess'][2])
        config['preprocess'] = 'python -u ' + ' '.join(config['preprocess'])

    # model file to uri
    if 'model_uri' not in config:
        config['model_uri'] =  urlparse.urljoin('file:', urllib.pathname2url(config['model_file']))

    # clean up output folder
    output_dir = os.path.join(config['output_dir'])
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        time.sleep(1)

    logging.info('Config file: ' + str(config))

def concatenate_output(output_file, output_dir):
    success_file = os.path.join(output_dir, '_SUCCESS')
    if not os.path.exists(success_file):
        logging.error('no _SUCCESS file in ' + output_dir)
        return

    with open(output_file, 'w') as outfile:
        for name in os.listdir(output_dir):
            file = os.path.join(output_dir, name)
            if os.path.isfile(file) and name.startswith('part-'):
                with open(file) as infile:
                    for line in infile:
                        outfile.write(line)

def zip_file(file, delete_after_zip = False):
    with zipfile.ZipFile(file + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write(file, os.path.basename(file))
    if delete_after_zip:
        os.remove(file)

def csv_to_json(csvfile_path, jsonfile_path):
    with open(csvfile_path, 'rbU') as csvfile:
        with codecs.open(jsonfile_path, 'w') as jsonfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                jsonfile.write(json.dumps(row) + '\n')


if __name__ == '__main__':

    # get config file
    config_module = import_module(sys.argv[1])
    logging.basicConfig(level = config_module.LOG_LEVEL)

    # init spark and jvm
    sc = SparkContext(appName = 'Auto AAC Workflow')
    java_import(sc._jvm, 'edu.isi.karma')

    file_util = FileUtil(sc)
    workflow = Workflow(sc)

    # clean up previous consolidated data
    consolidated_file = os.path.join(config_module.repo_path, 'consolidated_data.n3')
    consolidated_file_zip = os.path.join(config_module.repo_path, 'consolidated_data.n3.zip')
    if os.path.exists(consolidated_file):
        os.remove(consolidated_file)
    if os.path.exists(consolidated_file_zip):
        os.remove(consolidated_file_zip)

    logging.info('Number of model: %d' % len(config_module.REPO_CONFIG))
    for config in config_module.REPO_CONFIG:
        init_repo_config(config)

        # Read the input
        logging.info('read input file: ' + config['input_file'])

        # preprocess
        if config['preprocess']:
            logging.info('preprocessing: ' + config['preprocess'])
            subprocess.call(config['preprocess'], shell=True)

        # process
        if config['input_file_type'] == 'csv':
            if not config['csv_to_jl']:
                input_rdd = workflow.batch_read_csv(config['input_file']).repartition(config['num_partitions'])
            else:
                csv_to_json(config['input_file'], config['input_file'] + '.jl')
                config['input_file'] = config['input_file'] + '.jl'
                config['input_file_type'] = 'jsonlines'
        
        if config['input_file_type'] == 'json':
            input_rdd = sc.wholeTextFiles(config['input_file']).mapValues(lambda x: json.loads(x))
        elif config['input_file_type'] == 'xml':
            input_rdd = sc.wholeTextFiles(config['input_file'])
        elif config['input_file_type'] == 'jsonlines':
            config['input_file_type'] = "json"
            input_rdd = sc.textFile(config['input_file']).map(lambda x: ("test", json.loads(x)))

        input_rdd = input_rdd.repartition(config['num_partitions']) 
        
        # Apply the karma Model
        logging.info('apply karma model')
        output_rdd = workflow.run_karma(
            input_rdd,
            config['model_uri'],
            config['base_uri'],
            config['rdf_root_uri'],
            config['context_uri'],
            num_partitions = config['num_partitions'],
            data_type = config['input_file_type'],
            batch_size = 500,
            additional_settings = config['additional_settings']
        )

        # Save the output
        # output_rdd.values().saveAsTextFile(config['output_file'])
        #output_rdd.values().distinct().saveAsTextFile(config['output_dir'])
        output_rdd.map(lambda x: x[1]).saveAsTextFile(config['output_dir'])

        # concatenate partitions to a single file
        concatenate_output(config['output_file'], config['output_dir'])

        # concatenate to consolidated data
        with open(consolidated_file, 'a') as output:
            with open(config['output_file'], 'r') as input:
                for line in input:
                    output.write(line)

        # zip and delete
        zip_file(config['output_file'], True)

    # zip consolidated data
    zip_file(consolidated_file, True)

