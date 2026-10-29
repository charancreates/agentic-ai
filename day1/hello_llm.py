import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="../.env", override=True)
my_api_key=os.getenv("GROQ_API_KEY")


if not my_api_key:
    raise ValueError("API Key nahi h bro")

client=Groq(api_key=my_api_key)

model =  os.getenv("MODEL")
role="user"
prompt="whats 2 + 2"
message={
    "role":role,
    "content":prompt
}
messages=[message]

response=client.chat.completions.create(
    model=model,
    messages=messages
)
print("###################################")
answer=response.choices[0].message.content
print(answer)