from .MessengerWebhook import MessengerWebhook
import sys

# __all__ = ["MessengerWebhook", "MessengerWebhookView"]

def InitMessenger(app, msgClass=MessengerWebhook):
    from .Messenger import endpoints, setApp
    app.messenger = msgClass(app, app.config["FB_MESSENGER_TOKEN"])
    app.register_blueprint(endpoints)
    setApp(app)