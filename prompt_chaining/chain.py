import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

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

JD=""""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

resume = """
Rahul
Software Developer with 3 years of experience.
Skills: Python, FastAPI, MySQL, Docker, REST APIs, Git.
Experience:
- Built scalable web APIs using Python and FastAPI.
- Managed containerized services with Docker.
"""

def ask_llm(system_prompt,user_prompt):
    sys_msg={
        "role":"system",
        "content":system_prompt
    }
    user_msg={
        "role":"user",
        "content":user_prompt
    }
    messages=[sys_msg,user_msg]
    response=client.chat.completions.create(model=model,messages=messages)
    answer=response.choices[0].message.content
    return answer

def step1_res_extact():
    system_prompt=""""
    You are a professional HR assistant. 
    Extract the skills from the candidate's resume provided.
    Only return the skills, no other information.
    Do not invent any skills by yourself.
    """
    user_prompt=f"""
    Extact the skills from this resume
    {resume}
    """
    
    return ask_llm(system_prompt,user_prompt)

def step2_jd_extact():
    system_prompt=""""
    You are a professional HR assistant. 
    Extract the skills from the candidate's JD provided.
    Only return the skills, no other information.
    Do not invent any skills by yourself.
    """
    user_prompt=f"""
    Extact the skills from this JD
    {JD}
    """
    
    return ask_llm(system_prompt,user_prompt)

def step3_match(candidate,jd):
    system_prompt=""""
        You are a professional HR assistant. 
        Compare the skills of candidate and the skills
        require in the jd , produce a final score between
        1 and 100. also produce a short verdict wheater the 
        candidate is good fit for the role
    """
    
    user_prompt=f"""
    Compare and match the skills
    jd:{jd}
    candidate:{candidate}
    """
    return ask_llm(system_prompt,user_prompt)
    
candidate = step1_res_extact()
# print(candidate)
sleep(2)
jd = step2_jd_extact()
# print(jd)
sleep(2)
score= step3_match(candidate,jd)
print(score)

    