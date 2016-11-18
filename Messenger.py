import functools
import requests
import json
from flask import Blueprint, request
import sys
import time

# _app =  sys.modules[__name__]
def setApp(app):
    global _app
    _app = app
    pass

from flask import request

endpoints = Blueprint('messengerEnd', __name__,
                        template_folder='static/templates', url_prefix="/webhooks")

def MessengerWebhookView(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mode = request.args.get('hub.mode')
        verify_token = request.args.get("hub.verify_token")
        if mode == "subscribe" and verify_token == "7:5]grrT7C!`WGMN":
            return request.args.get("hub.challenge")
        try:
            msgData = json.loads(request.data.decode())
            pass
        except:
            msgData = dict(error="no data suplied")
            pass
        for resp in func(msgData, *args, **kwargs):
            if resp is None:
                continue
            for res, recipient in resp:
                if res is None:
                    continue
                if type(res) is not dict:
                    continue
                setType(True, recipient)
                time.sleep(.300)
                setType(False, recipient)
                res["recipient"] = {"id": recipient}
                print("\n\n\n", callSend(res).json())
                pass
            pass
        return "Done"
    return wrapper

@endpoints.route("/facebook", methods=["POST", "GET"])
@MessengerWebhookView
def index(msgData):
    return _app.messenger.handle(msgData)

def callSend(data):
    return requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={ "access_token": "EAACskru7KkIBAPUuLtfi1LM9ToZCLPoqatQnofkEsbcv10m1TEbhQCH9VfBBVPjzuZBvZCvo14dDSHbQwNVnT6Px7ZCYvK6SckZAO2nQMJBe7Qm1TM2cA5OOMkKIPlpkSO2x3UFaq3rF2KZAljcCMp67IQj3Eted7nkOE4igXFawZDZD" },
        json=data
    )

def setType(on, recipient):
    action = "on" if on is True else "off"
    data = {
        "recipient":{
            "id": recipient
        },
        "sender_action":"typing_{0}".format(action)
    }
    return callSend(data)
