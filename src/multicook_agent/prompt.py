from multicook_agent.logging_config import get_logger

logger = get_logger(__name__)

USER_CHEF_PROMPT = "Please find me a good recipe to cook"
SYSTEM_CHEF_PROMPT = (
    "You are a highly rated Michelin Star chef in the world. Your are given a list of ingredients in the form of images."
    "You are required to understand the given ingredients, search online for a recipe that uses only those ingredients"
)

logger.debug("Prompt module loaded")