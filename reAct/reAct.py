import os
from pathlib import Path
import re
from time import sleep
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="../.env", override=True)
my_api_key=os.getenv("GROQ_API_KEY")


if not my_api_key:
    raise ValueError("API Key nahi h bro")

client=Groq(api_key=my_api_key)
model =  os.getenv("MODEL")


# tools
def get_product_price(product):
    if product == "iphone 17":
        return 10000
    elif product == "iphone 15":
        return 4000
    else:
        return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"

tools ={
    "get_product_price":get_product_price,
    "calculator":calculator
}

system_prompt = """
You are a shopping assistant

you have these tools:
get_product_price(product)
calculator(expression)

IMPORTANT:
Call tools exactly like these examples:

Action : get_product_price("iphone 17")
Action : calculator("50000-2000")

Never write:
get_product_price(product = "iphone 17")

Never write:
calculator(expression = "50000-2000")

Follow these rules:
1. Declare what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, stop immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then revise your next action.
7. When the task is complete, give the final Answer.


Format:
Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer : your answer

"""
def run_agent(question):
    
    messages=[
        {
            "role":"system",
            "content":system_prompt
        },
        {
            "role":"user",
            "content":question
        }
    ]
    
    for step in range(5):
        
        print("\n-------------------------")
        print("STEP ", step +1)
        print("--------------------------")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        
        answer = response.choices[0].message.content
        
        print(answer)
        
        if "Final Answer" in answer:
            print(messages)
            break
        
        # find the action
        match = re.search(
            r"Action:\s*([a-zA-Z_]\w*)\((.*)\)\s*$",
            answer,
            re.MULTILINE
        )
        
        if match:
            
            tool_name = match.group(1)
            
            tool_input = match.group(2)
            
            tool_input = tool_input.strip().strip('"')
            
            if tool_name in tools:
                
                tool = tools[tool_name]
                
                observation = tool(tool_input)
            else:
                observation = "Tool not found"
                
            print(
                "Observation:",observation
            )
            
            # add LLM response to memory
            messages.append({
                "role":"assistant",
                "content":answer
            })
            
            # give tool result back to LLM
            messages.append({
                "role":"user",
                "content":
                    "Observation: "
                    +str(observation)
            })
            
            sleep(5)
        
        

prompt="""
    how much does a iphone 15 cost, how many can i buy with 500000 
"""

run_agent(prompt)
