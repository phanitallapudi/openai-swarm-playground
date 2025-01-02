
from dotenv import load_dotenv
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders
from swarm import Swarm, Agent

import os

from app.utils.swarm_tools import send_email, get_weather, search_duckduckgo, generate_random_string, factorial, reverse_string, longest_word, is_palindrome, fibonacci_series, generate_random_color, get_current_datetime, count_words, read_txt_file, get_ip_address

load_dotenv(override=True)

PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
VIRTUAL_KEY = os.getenv("VIRTUAL_KEY")
PORTKEY_OPENAI_API_KEY = os.getenv("PORTKEY_OPENAI_API_KEY")

class SwarmManagement:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=PORTKEY_OPENAI_API_KEY, # defaults to os.environ.get("OPENAI_API_KEY")
            base_url=PORTKEY_GATEWAY_URL,
            default_headers=createHeaders(api_key=PORTKEY_API_KEY, virtual_key=VIRTUAL_KEY)
        )
        self.swarm_client = Swarm(client=self.client)

    def make_query(self, query):
        assistant_agent = Agent(
            name="Assistant Agent",
            instructions="Help the user with their queries and requests, use the functions if needed",
            functions=[get_weather, send_email, search_duckduckgo, generate_random_string, factorial, reverse_string, longest_word, is_palindrome, fibonacci_series, generate_random_color, get_current_datetime, count_words, read_txt_file, get_ip_address], # type: ignore
        )
        # Initialise Swarm client and run conversation
        response = self.swarm_client.run(
            agent=assistant_agent,
            messages=[{"role": "user", "content": query}],
        )

        response = {
            "message": response.messages[-1]["content"]
        }

        return response