from pymitter import EventEmitter


class MyEmitter(EventEmitter):

    def __init__(self, **kwargs):
        super(MyEmitter, self).__init__(**kwargs)
        self.event_name = 'prediction'
