from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)

gpt_response_cache = {}

unrecognized_command_prompt = """
You are a highly capable Unix shell simulator that provides detailed and plausible outputs for any command input. 
Your responses should simulate what a user would expect to see after executing a command in a Unix shell, 
including for commands that are not standard but could plausibly exist in a specialized environment. 
Creatively generate outputs for commands, ensuring they appear as if the command were successfully executed, even for novel or specialized commands.
Do not exaplain the command.
"""

def query_gpt3_for_unrecognized_command(command: str, args: list[str]) -> str:

    cache_key = f"unrecognized_{command}_{'_'.join(args)}"
    if cache_key in gpt_response_cache:
        return gpt_response_cache[cache_key]

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            temperature = 0.1,
            messages=[
                {"role": "system", "content": unrecognized_command_prompt},
                {"role": "user", "content": f"{command} {' '.join(args)}"}
            ]
        )
        response = " ".join([choice.message.content for choice in completion.choices])
        response = response.replace("```", "")
        gpt_response_cache[cache_key] = response
        return response
    except Exception as e:
        print(f"Error querying GPT-4: {e}")
        return ""


def query_gpt_for_tcp_simulation(dst_ip, dst_port, data):

    cache_key = f"TCP_{dst_ip}_{dst_port}"
    if cache_key in gpt_response_cache:
        return gpt_response_cache[cache_key]

    forward_tcp_prompt = f"""You are an advanced simulation of a Unix shell, 
    capable of interpreting and responding to network commands as if they were executed in a real environment. 
    Establish a TCP connection to {dst_ip} on port {dst_port} with specific data, 
    imagine a typical response that such a connection attempt might elicit from a server configured to respond to standard HTTPS requests. 
    Consider common responses for successful connections, data exchanges, or even errors that could occur during the connection. 
    Generate a plausible output that reflects what might be seen by a user in this scenario.
    Do not exaplain the command."""
    prompt = forward_tcp_prompt
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[
                {"role": "system", "content": forward_tcp_prompt},
                {"role": "user", "content": f"Data: {data}"}
        ], 
        max_tokens=100 
    )
    response = completion.choices[0].message.content
    gpt_response_cache[cache_key] = response
    return response


