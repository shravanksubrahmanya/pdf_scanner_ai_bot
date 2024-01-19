from flask import current_app
from app.chat.callbacks.stream import StreamingHandler
from queue import Queue
from threading import Thread

class StreamableChain: #StreamingChain(LLMChain):

    '''Overriding the streaming function of a chain'''
    def stream(self,input):
        queue=Queue()
        handler = StreamingHandler(queue) # this handler is created for current call

        def task(app_context):
            '''# running a chain, reference to the current class. and assigning handler to
            current request'''
            app_context.push()
            self(input, callbacks=[handler])
        
        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get() # fetching the firat element.
            if token is None:
                break
            yield token