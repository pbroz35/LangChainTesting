import json
import os
import openai
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# functions
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    },
    
    {
        
        "name": "get_current_temperature",
        "description": "Get the current temperature in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },    
    },
]

messages = [
    {
        "role": "user",
        "content": "What's the weather like in Boston in fahrenheit?"
    }
]


#main

openai.api_key = os.environ['OPENAI_API_KEY']
client = OpenAI()

# print(openai.api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions,
    function_call ="auto", # "auto" can choose to force the model to call a function "none" - forces model to NOT use any function calls 
)

print(response)


function_call = response.choices[0].message.function_call
args = json.loads(function_call.arguments)


def get_current_weather(location): #assuming location is Boston Ma, function would need to get actual weather based off a location
    return "The current weather is sunny and in the high 80's."


#simulate calling the function based off the ai response (function would need to be defined)
observation = get_current_weather(args.get("location"))

messages.append(
    {
         "role": "function",
         "name": "get_current_weather",
         "content": observation,
     }
 )
#
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
 )
   
print(response)
