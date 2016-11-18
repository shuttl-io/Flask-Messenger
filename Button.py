class Button:

    def __init__(self, title, payload_url, tp="postback"):
        self.tp = tp
        self.title = title
        self.payload = payload_url
        pass

    def serialize(self):
        obj = "url" if self.tp=="web_url" else "payload"
        return {
            "type": self.tp,
            obj: self.payload,
            "title": self.title
        }
