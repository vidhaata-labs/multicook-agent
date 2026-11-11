import argparse
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent

from multicook_agent.logging_config import configure_logging, get_logger
from multicook_agent.model_config import create_llm, get_available_providers
from multicook_agent.photo_decoder import build_image_message, choose_image_files
from multicook_agent.prompt import SYSTEM_CHEF_PROMPT, USER_CHEF_PROMPT
from multicook_agent.tools import web_search
from multicook_agent.utils import extract_text_content
from rich.console import Console
from rich.markdown import Markdown

configure_logging()
logger = get_logger(__name__)
console = Console()

parser = argparse.ArgumentParser(description="MultiCook Agent - Recipe suggestion from ingredient images")
parser.add_argument(
    "--image",
    "-i",
    type=str,
    default=None,
    help="Path to an ingredients image file (skips the file picker)",
)
parser.add_argument(
    "--mode",
    "-m",
    type=str,
    choices=["single", "multi"],
    default="single",
    help="Image selection mode: single or multi (default: single)",
)
args = parser.parse_args()

logger.info("Available LLM providers: %s", get_available_providers())
logger.info("Configuring model...")
model = create_llm()

logger.info("Creating agent...")
agent = create_agent(
    model,
    tools=[web_search],
    system_prompt=SYSTEM_CHEF_PROMPT,
)

if args.image:
    from pathlib import Path

    image_path = Path(args.image)
    logger.info("Using provided image: %s", image_path)
else:
    from multicook_agent.photo_decoder import SelectionMode

    mode = SelectionMode.SINGLE if args.mode == "single" else SelectionMode.MULTI
    logger.info("Choosing ingredients image (mode=%s)...", mode.value)
    image_path = choose_image_files(mode=mode)

if isinstance(image_path, list):
    logger.info("Selected %d image(s)", len(image_path))
    for p in image_path:
        logger.info("  - %s", p)
else:
    logger.info("Selected image: %s", image_path)
message = build_image_message(image_path, USER_CHEF_PROMPT)

logger.info("Invoking agent...")
response = agent.invoke(
    {"messages": [message]},
)

content = extract_text_content(response["messages"][-1].content)
logger.info("Agent response received (%d characters)", len(content))
logger.info("Printing agent response...")
print("\n" + "=" * 60 + "\n")
console.print(Markdown(content))
logger.info("Agent response printed successfully.")
