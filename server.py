import json
import tornado.ioloop
import tornado.web
import database as db


def base10_to_62(base10_number):
    table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    while base10_number:
        result += table[base10_number % 62]
        base10_number = int(base10_number / 62)
    return result[::-1]


def get_original_url(shorted_url):
    info = db.mapping.find_one({
        'shorted': shorted_url
    })
    if not info:
        return None
    return info['original']


def generate_short_url(original_url):
    if original_url[:7] != 'http://' and original_url[:8] != 'https://':
        return None
    info = db.mapping.find_one({
        'original': original_url
    })
    if info:
        return info['shorted']
    counter = db.counter.find_one_and_update({
        'name': 'counter'
    }, {
        '$inc': {'seq': 1}
    })['seq']
    shorted = base10_to_62(counter)
    db.mapping.insert({
        'original': original_url,
        'shorted': shorted,
    })
    return shorted


class New_Item(tornado.web.RequestHandler):

    def post(self):
        try:
            data = json.loads(self.request.body.decode())
        except ValueError:
            return self.finish(json.dumps({
                'error': 'Params error'
            }))
        if 'url' not in data:
            return self.finish(json.dumps({
                'error': 'Params error'
            }))
        shorted = generate_short_url(data['url'])
        if not shorted:
            return self.finish(json.dumps({
                'error': 'Params error'
            }))
        return self.finish(json.dumps({
            'original_url': data['url'],
            'shorted_url': shorted,
        }))


class Jump(tornado.web.RequestHandler):

    def get(self, shorted_url):
        original = get_original_url(shorted_url)
        if not original:
            self.redirect('/')
        self.redirect(original, permanent=True)


class Get_Original(tornado.web.RequestHandler):

    def post(self):
        try:
            data = json.loads(self.request.body.decode())
        except ValueError:
            return self.finish(json.dumps({
                'error': 'Params error'
            }))
        if 'url' not in data:
            return self.finish(json.dumps({
                'error': 'Params error'
            }))
        original = get_original_url(data['url'])
        if not original:
            return self.finish(json.dumps({
                'error': 'Not found'
            }))
        return self.finish(json.dumps({
            'original_url': original,
            'shorted_url': data['url'],
        }))


def make_app():
    return tornado.web.Application([
        (r'/api/new', New_Item),
        (r'/api/get_original_url', Get_Original),
        (r'/([a-z0-9A-Z]+)', Jump),
    ])


def init_database():
    result = db.counter.find_one({
        'name': 'counter'
    })
    if not result:
        db.counter.insert({
            'name': 'counter',
            'seq': 916132832,  # base10 916132832 = base64 100000
        })


if __name__ == '__main__':
    init_database()
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
