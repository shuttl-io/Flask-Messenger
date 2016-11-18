import requests
import json

def callSend(userId):
    user = requests.get(
        "https://graph.facebook.com/v2.6/{0}".format(userId),
        params={ "access_token": "EAACskru7KkIBAPUuLtfi1LM9ToZCLPoqatQnofkEsbcv10m1TEbhQCH9VfBBVPjzuZBvZCvo14dDSHbQwNVnT6Px7ZCYvK6SckZAO2nQMJBe7Qm1TM2cA5OOMkKIPlpkSO2x3UFaq3rF2KZAljcCMp67IQj3Eted7nkOE4igXFawZDZD" },
    ).json()
    user["id"] = userId
    return user

class Sender:
    def __init__(self, id):
        self.id = id
        pass

class MessengerWebhook:
    def __init__(self, app, token):
        self.app = app
        self._create(token)
        pass

    def _create(self, token):
        self.token = token
        pass

    def handle(self, data):
        if data.get("object") != "page":
            return
        for page in data["entry"]:
            page_id = page ["id"]
            for event in page ["messaging"]:
                recipient = event["sender"]["id"]
                print ("\n\n\nEvent:", event)
                res = self._handleEvent(page_id, event)
                res = [res] if not hasattr(res, '__iter__') else res
                res = [(i, recipient) for i in res]
                yield res
            pass
        pass

    def _handleEvent(self, page_id, event):
        user = self.loadUser(event)
        args = [page_id, event, user]
        if event.get("optin") is not None:
            return self.optin(*args)
        if event.get("message") is not None:
            return self.handleMessage(*args)
        if event.get("delivery") is not None:
            return self.deliveryConfirmation(*args)
        if event.get("postback") is not None:
            return self.postback(*args)
        return None

    def loadUser(self, event):
        user_info = callSend(event["sender"]["id"])
        return user_info

    def text(self, page_id, event, user):
        raise NotImplementedError

    def attachment(self, page_id, event, user):
        raise NotImplementedError

    def handleMessage(self, *args):
        if args[1]["message"].get("attachments") is not None:
            return self.attachment(*args)
        elif args[1]["message"].get("text") is not None:
            return self.text(*args)
        raise NotImplementedError

    def optin(self, page_id, event, user):
        raise NotImplementedError

    def message(self, page_id, event, user):
        raise NotImplementedError

    def deliveryConfirmation(self, page_id, event, user):
        raise NotImplementedError

    def postback(self, page_id, event, user):
        raise NotImplementedError

    def addQuickReply(self, cb, msg, **kwargs):
        cb_name = cb.__name__
        arguments = kwargs.get("arguments", {})
        args = json.dumps(arguments)
        cb_name = "{0}:{1}".format(cb_name, args)
        tp = kwargs.get("type", "text")
        title = kwargs.get("title")
        img = kwargs.get("img")
        if tp == "text" and title is None:
            raise TypeError("title cannot be none if type is text")
        content = {
            "content_type": tp,
            "payload": cb_name,
        }
        if title is not None:
            content["title"] = title
            pass
        if img is not None:
            content["image_url"] = img
            pass
        replies = msg["message"].get("quick_replies", list())
        replies.append(content)
        msg["message"]["quick_replies"] = replies
        return msg
