import datetime

from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

import twilio.twiml

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1/test'

db = SQLAlchemy(app)


class CallEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, phone_number):
        self.phone_number = phone_number


@app.route("/", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming requests."""
    from_number = request.values.get('From', 'Unknown')
    call_entry = CallEntry(from_number)
    db.session.add(call_entry)
    db.session.commit()
    resp = twilio.twiml.Response()
    resp.say("Hello Monkey")

    return str(resp)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
