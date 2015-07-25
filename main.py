# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import os
import sys
import json


class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, *args, **kwargs):
        if status_code == 404:
            self.write("OMG!! OMG!! 404!! Are you ok?!")
        else:
            tornado.web.RequestHandler.write_error(self, status_code, *args, **kwargs)


class MainHandler(BaseHandler):
    def get(self):
        files = os.listdir(os.path.join(".", "data"))
        self.render("main.html", files=files)
        
        
class WikiHandler(BaseHandler):
    def get(self, *args):
        with open(os.path.join(os.path.join(".", "data"), args[0] + ".json"), "rb") as file:
            data = file.read().decode("utf-8")
            data = json.loads(data)
            self.render("data.html", data=data)


class OtherHandler(BaseHandler):
    def get(self, *args, **kwargs):
        raise tornado.web.HTTPError(404)


route = [
    (r"/", MainHandler),
    (r"/wiki/(.*)", WikiHandler),
    (r"(.*)", OtherHandler)
]


app = tornado.web.Application(
    route,
    template_path=".",
    debug=True
)
app.listen(8889)
try:
    tornado.ioloop.IOLoop.current().start()
except:
    tornado.ioloop.IOLoop.current().stop()
