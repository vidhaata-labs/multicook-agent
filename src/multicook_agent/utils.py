from typing import Union

from multicook_agent.logging_config import get_logger

logger = get_logger(__name__)


def extract_text_content(content: Union[str, list]) -> str:
    """Extract plain text from a message content that may be a string or a list of blocks."""
    logger.debug("extract_text_content called with type=%s", type(content).__name__)
    if isinstance(content, str):
        logger.debug("extract_text_content returning string directly")
        return content
    parts: list[str] = []
    for block in content:
        if isinstance(block, dict):
            text = block.get("text") or block.get("content")
            if text:
                parts.append(text)
        elif isinstance(block, str):
            parts.append(block)
    result = "".join(parts)
    logger.debug("extract_text_content returning %d characters", len(result))
    return result
