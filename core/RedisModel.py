import redis
from config.RedisConfig import redisConfig

def connection():
    config = redisConfig()
    #reids连接池
    # pool = redis.ConnectionPool(host=config['host'], port=config['port'], decode_responses=True)
    # r = redis.Redis(host=config['host'], port=config['port'], decode_responses=True)
 
    r = redis.Redis(host=config['host'], port= config['port'], decode_responses=True,socket_connect_timeout=5)
    try:
        r.ping()
    except TimeoutError:
        print('redis connection timeout')
        
    return r