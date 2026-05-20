 

from dataclasses import dataclass

from litellm.types.completion import ChatCompletionMessageParam as Message


@dataclass
class SessionState:
    session_id:str
    messages:list[Message]
    system_prompt:str

    def addMessage(self,message:Message):
        self.messages.append(message)
    def build_messages(self)->list[Message]:
        messages:list[Message] =  [{"role":"system","content":self.system_prompt}]
        messages.extend(self.messages)
        return messages