#!/usr/bin/python
# -*- coding: utf-8 -*-
from sys import stderr
from time import sleep
from math import log
import argparse
import requests

spinner = ['|', '/', '-', '\\']

def spin(prompt, time):
    step = int(time / 0.125)
    for i in range(step):
        stderr.write('\r{}'.format(' ' * (len(prompt) + 1)))
        stderr.write('\r{}{}'.format(prompt, spinner[i % 4]))
        stderr.flush()
        sleep(0.125)
    stderr.write('\r{}'.format(' ' * (len(prompt) + 1)))
    stderr.write('\r{}Done\n'.format(prompt))
    stderr.flush()

def confirm(prompt):
    value = raw_input('{} (Y/n): '.format(prompt))
    return len(value) == 0 or confirm in ['y', 'Y', 'yes', 'Yes', 'YES']

def fetch(args):
    names = args.names
    for name in names:
        r = requests.get('https://api.imascg.moe/characters/{}'.format(name))
        item = r.json()
        if confirm('Do you want to fetch {}: {}'.format(item['id'], item['name'].encode('utf-8'))):
            spin('Fetching reference profile: {}...'.format(name), 5)
            with open('{}.yml'.format(item['id']), 'w') as f:
                f.write('id: {}\n'.format(item['id']))
                f.write('name: {}\n'.format(item['name'].encode('utf-8')))
        else:
            print 'Fetch cancelled'

def search(args):
    query = args.query

    r = requests.get('https://api.imascg.moe/characters?search={}'.format(query))

    items = r.json()

    print 'Found {} entries for {}'.format(len(items), query)

    for item in items:
        print '  {}: {}'.format(item['id'], item['name'].encode('utf-8'))

def create(args):
    config = args.config

    spin('Parsing information from {}...'.format(config), 0)
    spin('Fetching reference data...', 3)

    if not confirm('Are you sure you want to proceed?'):
        print 'Aborting'
        return

    spin('Synthesizing DNA...', 10)
    spin('Submitting DNA to Stork system', 3)
    print 'Your child should be delivered in a few days.'

def modify(args):
    config = args.config

    spin('Parsing information from {}...'.format(config), 0)
    spin('Fetching reference data...', 3)
    spin('Analyzing gene expression status...', 5)

    if confirm('Do you want to see the differential expression profile?'):
        print '| {:^22} | {:^7} | {:^7} |'.format('gene name', 'before', 'after')

        with open('E-GEOD-58387-query-results.tpms.tsv') as f:
            for line in f:
                F = line.rstrip().split('\t')

                if len(F) == 4:
                    _, name, after, before = F

                    if after == '':
                        after = '0.0'
                else:
                    _, name, after = F
                    before = '0.0'

                print '| {:<22} | {:>7} | {:>7} |'.format(name, before, after)

    if not confirm('Are you sure you want to proceed?'):
        print 'Aborting'
        return

    spin('Creating cocktail...', 5)
    spin('Deploying cocktail...', 7)
    stderr.write('Your expression profile should be modified promptly')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='girlbrew: brew your girl')
    subparsers = parser.add_subparsers(help='girlbrew subcommands')

    parser_fetch = subparsers.add_parser('fetch', description='fetch a reference profile')
    parser_fetch.add_argument('names', type=str, nargs='+', help='a reference profile to fetch')
    parser_fetch.set_defaults(func=fetch)

    parser_search = subparsers.add_parser('search', description='search for a reference profile')
    parser_search.add_argument('query', type=str, help='reference profile to search')
    parser_search.set_defaults(func=search)

    parser_create = subparsers.add_parser('create', description='create your own designed baby')
    parser_create.add_argument('config', type=str, help='configuration file')
    parser_create.set_defaults(func=create)

    parser_modify = subparsers.add_parser('modify', description='modify your expression profile')
    parser_modify.add_argument('config', type=str, help='configuration file')
    parser_modify.set_defaults(func=modify)

    args = parser.parse_args()
    args.func(args)
