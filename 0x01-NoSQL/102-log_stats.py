#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


if __name__ == "__main__":
    # connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017/')

    # get the logs database and nginx collection
    logs = client.logs
    nginx = logs.nginx

    # count the total number of logs
    count = nginx.count_documents({})

    print(f"{count} logs")

    # count the number of logs for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = nginx.count_documents({"method": method})
        print(f"method {method}: {method_count}")

    # count the number of logs with method=GET and path=/status
    status_count = nginx.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_count} status check")

    # count the top 10 IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = nginx.aggregate(pipeline)

    print("IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")

