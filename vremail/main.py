#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from models import Mail
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
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')

        usr_mail = user.email()
        email_check = Mail.query().fetch(projection=[Mail.od])

        if email_check == usr_mail:
            email_data = Mail.query().fetch()
            params = {"logout_url": logout_url, "user": user, "email_data": email_data}
            return self.render_template("vremail.html", params=params)
        else:
            params = {"logout_url": logout_url, "user": user}
            return self.render_template("vremail.html", params=params)

    def post(self):
        user = users.get_current_user()

        od = self.request.get(utils.escape("od"))
        if len(od) == 0:
            od = user.email()
        do = self.request.get(utils.escape("do"))
        sporocilo = self.request.get(utils.escape("sporocilo"))
        usr_id = user.user_id()
        email = Mail(od=od, do=do, sporocilo=sporocilo, user_ID= usr_id)

        if email is not None:
            email.put()
            info = {"user": user,"uspeh": u"Sporočilo uspešno poslano"}

            return self.render_template("vremail.html", params=info)

class PoslanoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        email_data = Mail.query(Mail.izbrisan == False).fetch()

        params = {"logout_url": logout_url, "user": user, "email_data": email_data}
        return self.render_template("poslano.html", params=params)

class PrejetoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        email_data = Mail.query(Mail.izbrisan == False).fetch()

        params = {"logout_url": logout_url, "user": user, "email_data": email_data}
        return self.render_template("prejeto.html", params=params)

class VremeHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')

        params = {"logout_url": logout_url, "user": user}
        return self.render_template("vreme.html", params)

class DeleteHandlerPoslano(BaseHandler):
    def get(self, mail_id):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        mail = Mail.get_by_id(int(mail_id))

        params = {"logout_url": logout_url, "user": user,"mail_id": mail}
        return self.render_template("poslano.html", params=params)

    def post(self, mail_id):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        email_data = Mail.query(Mail.izbrisan == False).fetch()
        mail = Mail.get_by_id(int(mail_id))

        mail.izbrisan = True
        mail.put()

        params = {"logout_url": logout_url, "user": user,"email_data":email_data, "izbris": u"Sporočilo uspešno izbrisano"}
        return self.render_template("poslano.html", params=params)


class DeleteHandlerPrejeto(BaseHandler):
    def get(self, mail_id):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        mail = Mail.get_by_id(int(mail_id))

        params = {"logout_url": logout_url, "user": user, "mail_id": mail}
        return self.render_template("prejeto.html", params=params)

    def post(self, mail_id):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        email_data = Mail.query(Mail.izbrisan == False).fetch()
        mail = Mail.get_by_id(int(mail_id))

        mail.izbrisan = True
        mail.put()

        params = {"logout_url": logout_url, "user": user, "email_data": email_data, "izbris": u"Sporočilo uspešno izbrisano"}
        return self.render_template("poslano.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vremail', VremailHandler),
    webapp2.Route('/vreme', VremeHandler),
    webapp2.Route('/poslano', PoslanoHandler),
    webapp2.Route('/prejeto', PrejetoHandler),
    webapp2.Route('/prejeto/<mail_id:\d+>', DeleteHandlerPrejeto ),
    webapp2.Route('/poslano/<mail_id:\d+>', DeleteHandlerPoslano ),
], debug=True)

# pisanje v bazo (pseudo koda) ---> delete handler
#     pokliče stolpec Mail.izbrisani_id
#     preveri če je prazen
#         če je: doda ID uporabnika, ki je izbrisal mail + vejico
#         če ni: s for zanko se sprehodiš čez Mail.izbrisani_id in ga razdeliš na list
#                 my_string = 'A,B,C,D,E'
#                 my_list = my_string.split(",")
#                 ['A', 'B', 'C', 'D', 'E']
#                 preveri če je user.id() v listi #(for item in range(len(my_list)))
#                     če je: pass
#                     če ni: dodaj id v listo -> append(id)
#                             lista v string --> myList = ','.join(map(str, myList))
#                             shrani string v Mail.izbrisani_id
#
#
# branje baze (pseudo koda) ---> prejeto / poslano handler
#     pokliče stolpec Mail.izbrisani_id
#     preveri če je prazen
#         če je: pošlje None v template --> da se prikažejo vsi maili
#         če ni: pošlji string v template // ali array?
#
#
# jinja filtriranje glede na listo idjev --> prejeto/poslano template (wrap okoli že obstoječe kode)
#     dobi string iz prejeto/poslano handlerja
#     razdeli string v listo
#         # {% set list1 = variable1.split(';') %}
#         # {% for list in list1 %}
#         # <p>{{ list }}</p>
#         # {% endfor %}
#     vmes preveri, če se id v listi ujema s user.id()
#         če se: pass izpis tega maila
#         če ne: nadaljuje izpis