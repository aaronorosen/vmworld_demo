import datetime
import socket

from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

import twilio.twiml

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mesos:mesos@10.0.0.3/mesos'

db = SQLAlchemy(app)


class CallEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    hostname = db.Column(db.String(255))

    def __init__(self, phone_number, hostname):
        self.phone_number = phone_number
        self.hostname = hostname


@app.route("/", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming requests."""
    from_number = str(request.values.get('From', 'Unknown'))
    if from_number is not 'Unknown':
        # blur out last 3 digits:
        from_number = from_number[:len(from_number)-3] + "xxx"
    call_entry = CallEntry(from_number, socket.gethostname())
    db.session.add(call_entry)
    db.session.commit()
    resp = twilio.twiml.Response()
    resp.say("Hello world")
    return str(resp)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
