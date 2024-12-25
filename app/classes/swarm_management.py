
from swarm import Swarm, Agent
from dotenv import load_dotenv

from app.utils.swarm_tools import send_email, get_weather, search_duckduckgo, generate_random_string, factorial, reverse_string, longest_word, is_palindrome, fibonacci_series, generate_random_color, get_current_datetime, count_words, read_txt_file, get_ip_address

class SwarmManagement:
    def __init__(self) -> None:
        self.swarm_client = Swarm()
        load_dotenv()

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