import redis

client = redis.Redis(host='localhost', port=6379, db=0)

client.set('foo', 'barśćż')

value = client.get('foo')
print()
print(value)
print("-----------")
print(value.decode('utf-8'))
print("-----------")
print(value)