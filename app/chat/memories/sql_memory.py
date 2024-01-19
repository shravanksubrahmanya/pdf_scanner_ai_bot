from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory

# modules which are already created
# Gets all message tied to conversation | Adds a single message to the conversation.
from app.web.api import get_messages_by_conversation_id, add_message_to_conversation

class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str

    @property
    def messages(self):
        return get_messages_by_conversation_id(self.conversation_id)
    
    def add_message(self, message):
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content,
        )
    
    def clear(self) -> None:
        return super().clear()
    

def build_memory(chat_args):
    '''We are going to override default message chat memory with default SqlMessageHistory'''
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer",
    )