from functools import partial
from .chatopenai import build_llm

'''
when we call partial we pass in a function and some keyword arguments.
 it gives us back a brand new function.

 when we call a new function we are going to run the original function with any additional arguments 
 we provide to it.

 eg: build_llm(chat_args, model_name)

 that function is also going to receive any additional arguments we put with partial
'''

llm_map={
    "gpt-4":partial(build_llm, model_name="gpt-4"),
    "gpt-3.5-turbo":partial(build_llm, model_name="gpt-3.5-turbo"),
}

# builder = llm_map["gpt-4"]
# builder(chat_args)