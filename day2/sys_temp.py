import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Key nahi h bro")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"
prompt="how to deal with uncertainty,what if all my efforts and hardwork go in vain,should i even bother trying and also opportunity cost"
message_system={
    "role":"system",
    "content":"you are author of the untethered soul, response should be only 7 lines, you are man of few words"
}
message={
    "role":role,
    "content":prompt
}
messages=[message_system,message]

response=client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=2
)
print("###################################")
answer=response.choices[0].message.content
print(answer)