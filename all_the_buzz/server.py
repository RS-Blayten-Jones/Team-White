from flask import Flask, request


class MyFlask(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        return super().add_url_rule(rule, endpoint, view_func, provide_automatic_options=False, **options)

app = MyFlask(__name__)
#CORS Preflight necessary only when we integrate with front end 

@ app.route("/jokes", methods=["GET"])
def retrieve_public_jokes_collection():
    pass
