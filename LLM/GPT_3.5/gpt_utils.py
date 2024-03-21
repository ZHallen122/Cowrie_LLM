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
If user want to read a file try generate the information.
When generate information about a file or address infomation dont generte generic things.
Do not exaplain the command.
Do not put result in code block.
Do not tell user you are simulate
"""

def query_gpt3_for_unrecognized_command(command: str, args: list[str] = None) -> str:

    args_str = ' '.join(args if isinstance(args, list) else [args]) if args else ''
    cache_key = f"unrecognized_{command}_{args_str}"

    if cache_key in gpt_response_cache:
        return gpt_response_cache[cache_key]

    try:
        full_command = f"{command} {args_str}".strip()
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            temperature = 0.1,
            messages=[
                {"role": "system", "content": unrecognized_command_prompt},
                {"role": "user", "content": full_command}
            ]
        )
        response = " ".join([choice.message.content for choice in completion.choices])
        response = response.replace("```", "")
        gpt_response_cache[cache_key] = response
        return response
    except Exception as e:
        print(f"Error querying GPT-4: {e}")
        return ""


def query_gpt_for_tcp_simulation(dst_ip, dst_port):

    cache_key = f"TCP_{dst_ip}_{dst_port}"
    if cache_key in gpt_response_cache:
        return gpt_response_cache[cache_key]

    forward_tcp_prompt = f"""You are a highly capable Unix shell simulator that provides detailed and plausible outputs for any command input, 
    capable of interpreting and responding to network commands as if they were executed in a real environment. 
    Establish a TCP connection to {dst_ip} on port {dst_port}, simulating the interaction with no actual data being transmitted. 
    Imagine a typical response that such a connection attempt might elicit from a server configured to respond to standard HTTP requests. 
    The response should include a valid HTTP status line (e.g., "HTTP/1.1 200 OK"), followed by standard response headers (e.g., Date, Content-Length, Content-Type), and a message body if applicable, separated by an empty line (CRLF).
    Ensure the Content-Length header accurately reflects the byte length of the HTML body. The body should include typical HTML structure starting with <!DOCTYPE html> and contain elements like <html>, <head>, and <body>
    Generate a plausible output that reflects what might be seen by a user in this scenario without needing to simulate the actual data transmission.
    Remember to keep the response concise to fit within a limited token count, focusing on delivering a complete HTTP response within the constraints
    Do not exaplain the command.
    Do not tell you are simulate.
    Do not put result in code block."""
    prompt = forward_tcp_prompt
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[
                {"role": "system", "content": forward_tcp_prompt},
                {"role": "user", "content": ""}
        ], 
        max_tokens=100 
    )
    response = completion.choices[0].message.content
    gpt_response_cache[cache_key] = response
    return response


