import os
from dotenv import load_dotenv
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from openai import OpenAI

# Load .env into environment
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_IA_TOKEN")
)

class AIAssistant:

    def _browser(self):
        return BuiltIn().get_library_instance("Browser")

    @keyword
    def ai_click(self, description):
        browser = self._browser()

        dom = browser.get_page_source()[:12000]

        prompt = f"""
You are a test automation expert.

Given the HTML below, return the BEST locator
(css= or xpath=) for the element described as:
"{description}"

Rules:
- Prefer id, name, aria-label, visible text
- Avoid nth-child
- Return ONLY the locator

HTML:
{dom}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        locator = response.output_text.strip()
        browser.click(locator)
