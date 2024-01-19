from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.callbacks.base import BaseCallbackHandler # importing handler
from queue import Queue
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

class StreamingHandler(BaseCallbackHandler):
    '''
    Note: once every token is assembles inside streaming handler then it will be finally passed on
    to chain.
    '''

    def __init__(self, queue) -> None:
        self.queue = queue

    # the below function will be automatically called when streaming.
    def on_llm_new_token(self, token, **kwargs):
        # print(token)
        self.queue.put(token)
    
    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)
    
    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)

chat = ChatOpenAI(
    streaming=True,
    # callbacks=[StreamingHandler()], # adding handler for chat streaming. but here everyone is going to use the exact same copy of the streaming handler.
    )

prompt = ChatPromptTemplate.from_messages([
    ("human","{content}")
])

# chain = LLMChain(
#     llm=chat,
#     prompt=prompt,
# )

class StreamableChain: #StreamingChain(LLMChain):

    '''Overriding the streaming function of a chain'''
    def stream(self,input):
        queue=Queue()
        handler = StreamingHandler(queue) # this handler is created for current call

        def task():
            '''# running a chain, reference to the current class. and assigning handler to
            current request'''
            self(input, callbacks=[handler])
        
        Thread(target=task).start()

        while True:
            token = queue.get() # fetching the firat element.
            if token is None:
                break
            yield token

class StreamingChain(StreamableChain, LLMChain):
    '''It's a brand new class of all the functionalities of StreamableChain
    and LLMChain Put together.
    We can use this method in case we want to use multiple type of chains 
    ex. ConversationalChain etc.
    Now StreamableChain is taken as a Mixin
    '''
    pass

# class StreamingConversationalChain(StreamableChain, ConversationalRetrievalChain):
#     pass

chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content":"Tell me a joke"}):
    print(output)

# output = chain("Tell me a joke.")

# print(output)

# input = {"content":"Tell me a joke"}
# for output in chain.stream(input=input):
#     print(output)

# messages = prompt.format_messages(content="Tell me a big joke")

# output = chat(messages)
# output = chat.__call__(messages)
# output = chat.stream(messages)

# print(output)

# for message in chat.stream(messages):
#     print(message.content)