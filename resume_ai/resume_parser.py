import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv(dotenv_path="../.env", override=True)
my_api_key=os.getenv("GROQ_API_KEY")


if not my_api_key:
    raise ValueError("API Key nahi h bro")

client=Groq(api_key=my_api_key)
model =  os.getenv("MODEL")


job_description="""
BE/BTech/MCA or equivalent technical education.

Strong programming fundamentals and problem-solving ability.

Working knowledge of at least one language such as Python, JavaScript/TypeScript, Java or similar.

Basic understanding of APIs, databases, Git and Linux.

Curiosity about cloud, infrastructure, automation, Kubernetes and AI.

Ability to learn unfamiliar technologies independently and ask good technical questions.

Evidence that you build things: academic projects, GitHub work, internships, hackathons or personal projects.

What Matters More Than a Long Skills List

Fundamentals + curiosity + learning speed + ownership + ability to turn an idea into working software.
"""

class JobDescription(BaseModel):
    role:str
    required_skills:list[str]
    preferred_skills:list[str]
    minimum_experience:float|None
    education_requirements:list[str]
    responsibilites:list[str]
    
jobD_schema = JobDescription.model_json_schema()

system_prompt = f""""
    You are an expert HR assistant.

Your job is to analyze job descriptions and extract
structured information from them.

Return ONLY valid JSON matching this schema:

{jobD_schema}

IMPORTANT:
Do NOT return the schema itself.
Do NOT return fields like "properties", "title" or "type".
Fill the schema with actual information extracted from the job description.

If minimum experience is not mentioned, return null.
If information for a list is missing, return an empty list.
Do not invent information.

"""

user_prompt = f""""
Analyze the following job description
{job_description}
"""

message_system={
    "role":"system",
    "content":system_prompt
}

message_user={
    "role":"user",
    "content":user_prompt
}

response_format = {
    "type":"json_object"
}

messages=[message_system,message_user]

response=client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)
print("###################################")
answer=response.choices[0].message.content
# print(answer)


raw_json = answer

import json
job_data = json.loads(raw_json)

job = JobDescription(**job_data)