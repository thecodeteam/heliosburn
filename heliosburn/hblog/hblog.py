# hblog is a daemon that subscribes to a redis pubsub queue, where hb-related log events are published. These events are
# recieved by hblog and re-published to mongodb, where they persist.

redis_host = 'localhost'
redis_port = 6379
redis_queue = 'hblog'

mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_database = 'heliosburn'

def main():
    import json
    import redis
    from pymongo import MongoClient
    print(">> connecting to redis")
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    s = r.pubsub()
    s.subscribe(redis_queue)

    print(">> connecting to mongodb")
    client = MongoClient(host=mongodb_host, port=mongodb_port)
    dbc = client[mongodb_database]
    for msg in s.listen():
        if ('type' in msg) and (msg['type'] == 'subscribe'):  # Discard subscription success message
            print(">> subscribed to pubsub queue '%s'" % redis_queue)
            continue
        print("Received msg '%s'" % msg)
        try:
            data = json.loads(msg['data'])
            dbc.log.insert(data)
        except ValueError:
            print("!! could not deserialize JSON: %s" % msg['data'])


if __name__ == "__main__":
    main()