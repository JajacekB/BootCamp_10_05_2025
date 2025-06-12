def connect(**opcje):
    print(opcje)
    print(type(opcje))
    param = {
        'host': '127:0:0:1',
        'port': '8080'
    }
    param.update(opcje)
    print(param)
    param['pwd'] = opcje
    print(param)


connect()
connect(z=9)
connect(a=9, name="Radek")


def connect_all(*args, **kwargs):
    print(args, kwargs)


connect_all()
connect_all(1, 2, 3)
connect_all(1, 2, 3, 4, 5, 6)
connect_all(1, 2, 3, 4, 5, 6, "Zenek")
connect_all(1, 2, 3, 4, 5, 6, "Zenek", a=9, b=89)
connect_all(d=9, name="Tomek")