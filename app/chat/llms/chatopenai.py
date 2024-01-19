from langchain.chat_models import ChatOpenAI

def build_llm(chat_args, model_name):
    '''we can specify the llm to stream or not during the creation of the object for llm'''
    return ChatOpenAI(
        streaming=chat_args.streaming,
        # model_name="gpt-3.5-turbo" ---> default
        model_name=model_name,
        )