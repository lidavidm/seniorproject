import json
import webapp2
from google.appengine.ext import ndb


class Response(ndb.Model):
    responses = ndb.IntegerProperty(repeated=True)
    referrer = ndb.StringProperty()


class SubmitPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'

        try:
            form = json.loads(self.request.body)
            if not (isinstance(form, list) and len(form) == 11):
                raise ValueError("Form data must be list of length 11")

            answers = form[:10]
            referrer = form[-1]
            if not all(type(x) == int and (-1 <= x <= 3) for x in answers):
                raise ValueError("Form data must be list of ten integers from -1 to 3")

            response = Response(responses=answers,referrer=referrer)
            response.put()
        except ValueError as e:
            self.error(400)
            self.response.out.write("Invalid form submission: " + e.message + self.request.body)
            return

        self.response.out.write("True")


application = webapp2.WSGIApplication([
    ('/submit', SubmitPage),
], debug=True)