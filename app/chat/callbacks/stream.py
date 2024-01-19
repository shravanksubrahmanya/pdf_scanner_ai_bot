from langchain.callbacks.base import BaseCallbackHandler

class StreamingHandler(BaseCallbackHandler):
    '''
    Note: once every token is assembles inside streaming handler then it will be finally passed on
    to chain.
    '''

    def __init__(self, queue) -> None:
        self.queue = queue
        self.streaming_run_ids = set()

    def on_chat_model_start(self, serialized, messages, run_id,**kwargs):
        '''run_id => it is assigned to every execution of a lnaguage model.'''
        
        if serialized["kwargs"]["streaming"]:
            self.streaming_run_ids.add(run_id)

    # the below function will be automatically called when streaming.
    def on_llm_new_token(self, token, **kwargs):
        # print(token)
        self.queue.put(token)
    
    def on_llm_end(self, response, run_id,**kwargs):
        "this stops current llm execution but not chain"
        if run_id in self.streaming_run_ids:
            self.queue.put(None)
            self.streaming_run_ids.remove(run_id)
    
    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)