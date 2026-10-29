import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="../.env", override=True)
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Key nahi h bro")

client=Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role="user"


# structure it
from pydantic import BaseModel

class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    
schema = Ticket.model_json_schema()

response_format = {
    "type":"json_object"
}

system_prompt = f"""
    Extract the personal information from the ticket strictly based on this {schema} and give me a json output
"""

message_system={
    "role":"system",
    "content":system_prompt
}

text = "yo my name is sahil, i bought iphone duo , it folds and cracks, i need a refund, my email is sahilidk@gmail.com reach out to me . im from bangalore btw"
prompt=f"""
    This is a customer ticket , extract the personal information from this {text}
"""

message={
    "role":role,
    "content":prompt
}
messages=[message_system,message]

response=client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)


answer=response.choices[0].message.content
print(answer)


# reading it
import json

raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.email)