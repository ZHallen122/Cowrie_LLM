from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)

unrecognized_command_prompt = """
You are a highly capable Unix shell simulator that provides detailed and plausible outputs for any command input. 
Your responses should simulate what a user would expect to see after executing a command in a Unix shell, 
including for commands that are not standard but could plausibly exist in a specialized environment. 
Creatively generate outputs for commands, ensuring they appear as if the command were successfully executed, even for novel or specialized commands.
Do not exaplain the command.
"""

def query_gpt3_for_unrecognized_command(command: str, args: list[str]) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature = 0.1,
            messages=[
                {"role": "system", "content": unrecognized_command_prompt},
                {"role": "user", "content": f"{command} {' '.join(args)}"}
            ]
        )
        return " ".join([choice.message.content for choice in completion.choices])
    except Exception as e:
        print(f"Error querying GPT-3.5: {e}")
        return ""

# def query_gpt_for_tcp_simulation(dst_ip, dst_port, data):
#     prompt = f"Simulate a response for a TCP connection attempt to {dst_ip}:{dst_port} with data {data}."
#     response = client.completions.create(
#         model="gpt-3.5-turbo",
#         prompt=prompt,
#         temperature=0.5,  # Adjust as needed
#         max_tokens=100  # Adjust based on expected response length
#     )
#     return response.choices[0].text.strip()