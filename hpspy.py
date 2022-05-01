#!/usr/bin/env python

import argparse
#import importlib
#import Event as e
#import ROOT as r
#import os
#import sys
import yaml

from pyLCIO import IOIMPL

def parse_config(config_file) :
    print("Loading configuration from %s" % config_file)
    return yaml.load(open(config_file, 'r'), Loader=yaml.Loader)

def main() : 
   
    # Parse all command line arguments using the argparse module
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-c", action='store', dest='config',
                        help="Configuration file.")
    parser.add_argument("-n", action='store', dest='event_count', 
                        help="Total number of events.")
    parser.add_argument('-p', action='store', dest='print_freq', 
                         help='Freqency of event number printing.')
    args = parser.parse_args()

    if not args.config :
        parser.error('A configuration file needs to be specified.')

    # Set some defaults if the values are not specified
    event_count = args.event_count or -1
    print_freq = args.print_freq or 1000 

    # Parse the configuration file
    config = parse_config(args.config)

    files = []
    if "Files" in config:
        files = config["Files"]
    elif "FileList" in config: 
        flist = open(config["FileList"][0], 'r')
        for f in flist: 
            files.append(f.strip())

    ofile_path = config.get('OutputFile') or 'default.csv'
    print(ofile_path)

    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    print('Number of events %s' % reader.getNumberOfEvents())   
    ''' 
    analyses = config["Analyses"]
    analyses_instances = []
    for analysis in analyses : 
        analysis_module_name, analysis_class_name = analysis.rsplit(".", 1)
        print "[ ldmxpy ]: Adding analysis ==> Module: %s Class: %s" % (analysis_module_name, analysis_class_name)
        analysis_class = getattr(importlib.import_module(analysis_module_name), analysis_class_name)
        analyses_instances.append(analysis_class())

    ofile = root_open(ofile_path, 'recreate')
    
    params = {}
    if 'Parameters' in config: 
        params = config['Parameters']

    for analyses in analyses_instances : 
        analyses.initialize(params)
   
    tree_name = 'LDMX_Events'


    if 'TreeName' in config: 
        tree_name = config['TreeName'][0]

    event = e.Event(config)
    # Loop through all of the ROOT files and process them.
    for rfile_path in files :
        print 'Processing file %s' % rfile_path
        event.load_file(rfile_path, tree_name)
        
        event_counter = 0
        while event.next_event():
            for analysis in analyses_instances:
                analysis.process(event)
            event_counter += 1
            
            if event_counter == int(event_count): 
                print 'Hit event limit'
                break

            if event_counter%print_freq == 0: 
                print '[ ldmxpy ]: >> Event >> %s >>' % event_counter

        print "Total number of events processed: %s" % event_counter
        event.close_file()

    for analyses in analyses_instances : 
        analyses.finalize()
        
    ofile.close()
   '''
if __name__ == "__main__":
    main()
