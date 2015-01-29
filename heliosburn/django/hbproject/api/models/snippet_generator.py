# Snippet to generate traffic and store in Redis. Needed for traffic unit tests to be succesful.


def generate_traffic():
    import redis_wrapper
    import datetime
    import time
    import random
    import json

    current_milli_time = lambda: int(round(time.time() * 1000))

    def generate_request():
        methods = ['GET', 'PUT', 'DELETE', 'POST']
        statuses = [('200', 'OK'),
                    ('204', 'No Content'),
                    ('404', 'Not Found'),
                    ('201', 'Created'),
                    ('500', 'Internal Server Error')]
        urls = [
            'http://example.com/api/resource1/ob543',
            'http://example.com/api/account3/',
            'http://example.com/api/acco955/mycontainer0092',
            'http://example.com/api/acco955/mycontainer5/file.txt',
            'http://example.com/api/myacc/asdfg/dfofdg.mp3',
            'http://example.com/api/testaccount/testcontainer/helios.zip',
            'http://example.com/api/default_account/default_container'
        ]
        now = datetime.datetime.now()
        now.strftime('%Y-%m-%d %H:%M:%S')

        request = {}
        request['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['httpProtocol'] = "HTTP/1.1"
        request['method'] = random.choice(methods)
        request['url'] = random.choice(urls)
        request['response'] = {}
        request['response']['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['response']['httpProtocol'] = "HTTP/1.1"
        status = random.choice(statuses)
        request['response']['statusCode'] = status[0]
        request['response']['statusDescription'] = status[1]

        return json.dumps(request)

    r = redis_wrapper.init_redis()

    for i in range(1, 11):
        request = generate_request()
        score = current_milli_time()

        # Remove traffic older than 10 seconds
        result = r.zremrangebyscore('heliosburn.traffic', '-inf', score - 10*1000)
        print '* Cleaned %d messages' % (result,)

        # Add request to set
        result = r.zadd('heliosburn.traffic', score, request)
        print '* Message with score %d sent successfully' % (score, ) if result else 'Could not sent message (%d)' % (score,)

        print "Traffic piece #%d added" % i

if __name__ == "__main__":
    generate_traffic()