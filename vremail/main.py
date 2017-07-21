#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from models import Mail
from models import Vreme
from google.appengine.api import users
from jinja2 import utils

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')

            params = {"logiran": logiran, "logout_url": logout_url, "user": user}

        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url, "user": user}

        return self.render_template("main.html", params)

class VremailHandler(BaseHandler):

    def get(self):
        data = Mail.query().fetch()

        user = users.get_current_user()
        logout_url = users.create_logout_url('/')

        params = {"logout_url": logout_url, "user": user, "data": data}
        return self.render_template("vremail.html", params=params)

    def post(self):
        user = users.get_current_user()

        od = self.request.get(utils.escape("od"))
        if len(od) == 0 or od.isdigit():
            od = user
        do = self.request.get(utils.escape("do"))
        sporocilo = self.request.get(utils.escape("sporocilo"))
        prejeto = True #false je poslan mail
        email = Mail(od=od, do=do, sporocilo=sporocilo, prejeto= prejeto)

        if email != None:
            email.put()
            info = {"user": user,"uspeh": u"Sporočilo uspešno poslano"}

            return self.render_template("vremail.html", params=info)

class VremeHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        data = Vreme.query().fetch()

        params = {"logout_url": logout_url, "user": user, "data": data}
        return self.render_template("vreme.html", params)




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vremail', VremailHandler),
    webapp2.Route('/vreme', VremeHandler),
], debug=True)