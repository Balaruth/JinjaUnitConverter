#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")

class ConversionHandler(BaseHandler):
    def post(self):

        value = self.request.get("value")

        try:
            value = float(value)
            value2 = value * 0.621371
            conversion = str(value) + " kilometres is " + str(round(value2, 2)) + " miles."

        except ValueError:
            conversion = "Please enter a valid number to be converted!"

        return self.render_template("convert.html", params={"conversion": conversion})

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/convert', ConversionHandler),
], debug=True)
