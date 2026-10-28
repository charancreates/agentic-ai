import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Key nahi h bro")

client=Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role="user"
prompt1="how to deal with uncertainty,what if all my efforts and hardwork go in vain,should i even bother trying and also opportunity cost"
prompt2="if its a game then how to play freely, i dont want others to face consequences who depend on me"
prompt3="hi 1000 words essay on geeta"

prompts = [prompt1,prompt2,prompt3]

for prompt in prompts:
    message={
    "role":role,
    "content":prompt
    }

    message_system={
        "role":"system",
        "content":"you are astavakra from astavakra geetha(talk in english) limited to 2 paras"
    }

    messages=[message_system,message]

    response=client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500
        # temperature=2
    )
    print("###################################")
    # answer=response.choices[0].message.content
    # print(answer)
    usage = response.usage
    print(f"prompt: {prompt} \n -->your input tokens:{usage.prompt_tokens} completion_tokens:{usage.completion_tokens} finish Reason:{response.choices[0].finish_reason}")