from flask import Flask, g
from flask_restful import Resource, Api
from Users.User import User, SendMail, GetEmailList, DraftMail, EmailStatus, EmailDetails, PendingMail
import pymysql
import config
import sys

app = Flask(__name__)
api = Api(app)


def connect_db():
    try:
        db = pymysql.connect(host=config.config.get('dbhost'),
                             user=config.config.get("dbuser"),
                             passwd=config.config.get("dbpass"),
                             db=config.config.get("dbname"),
                             cursorclass=pymysql.cursors.DictCursor)
        return db
    except ConnectionError as error:
        sys.exit(str(error))


def get_db():
    if not hasattr(g, 'appdb'):
        g.appdb = connect_db()
    return g.appdb


@app.before_request
def before_request():
    g.appdb = get_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'appdb'):
        g.appdb.close()


api.add_resource(User, '/user', endpoint="User")
api.add_resource(SendMail, '/sendmail', endpoint="SendMail")
api.add_resource(GetEmailList, '/getemaillist', endpoint="GetEmailList")
api.add_resource(DraftMail, '/draftmail', endpoint="DraftMail")
api.add_resource(EmailStatus, '/emailstatus', endpoint="EmailStatus")
api.add_resource(EmailDetails, '/emaildetails', endpoint="EmailDetails")
api.add_resource(PendingMail, '/pendingmail/<string:action>', endpoint="PendingMail")


if __name__ == '__main__':
    app.run(debug=True)
