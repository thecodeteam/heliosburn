if __name__ == "__main__":

    import redis_wrapper
    import json

    r = redis_wrapper.init_redis(0)

    # initialized to 0 to obtain all available traffic for the first time
    last_time = 0

    while True:

        # gets the new traffic
        traffic = r.zrangebyscore('heliosburn.traffic', last_time, '+inf', withscores=True)
        print "* Received %d requests" % (len(traffic), )

        for message in traffic:
            request = json.loads(message[0])
            time_millis = int(message[1])

            # update the last_time to obtain new traffic the next time
            if time_millis > last_time:
                last_time = time_millis + 1  # increment by 1 to avoid getting the last request

            print "\t%d - Request: %s %s | Response: %s %s" % (
                time_millis, request['method'], request['url'], request['response']['statusCode'],
                request['response']['statusDescription'])

        raw_input("Press key to get more traffic...")