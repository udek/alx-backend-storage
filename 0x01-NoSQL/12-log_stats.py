#!/usr/bin/env python3
'''Provides some stats about Nginx logs stored in MongoDB.
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs.
    '''
    # Print the number of logs in the collection
    num_logs = nginx_collection.count_documents({})
    print('{} logs'.format(num_logs))

    # Print the number of logs for each HTTP method
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print('Methods:')
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, req_count))

    # Print the number of logs for GET requests to the /status path
    status_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(status_count))


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    # Connect to the MongoDB instance
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Retrieve the nginx collection and print the logs
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)


if __name__ == '__main__':
    run()

