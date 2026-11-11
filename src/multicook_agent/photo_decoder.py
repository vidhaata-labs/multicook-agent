from enum import Enum

import base64
import mimetypes

from pathlib import Path
from tkinter import TclError, Tk, filedialog
from langchain.messages import HumanMessage

from multicook_agent.logging_config import get_logger

logger = get_logger(__name__)


class SelectionMode(Enum):
    SINGLE = "single"
    MULTI = "multi"


def choose_image_files(mode: SelectionMode = SelectionMode.SINGLE) -> Path | list[Path]:
    """Open a local file picker when no image path is passed on the command line.

    mode: SelectionMode.SINGLE returns one Path, SelectionMode.MULTI returns a list of Paths.
    """
    logger.info("Opening file picker (mode=%s)", mode.value)
    root = None
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        filetypes = [
            ("Images", "*.png *.jpg *.jpeg *.webp"),
            ("All files", "*.*"),
        ]
        if mode == SelectionMode.MULTI:
            filenames = filedialog.askopenfilenames(
                title="Choose image",
                filetypes=filetypes,
            )
        else:
            filenames = filedialog.askopenfilename(
                title="Choose image",
                filetypes=filetypes,
            )
    except TclError:
        prompt_text = "Image path(s)" if mode == SelectionMode.MULTI else "Image path"
        path = input(f"{prompt_text}: ").strip().strip('"').strip("'")
        if mode == SelectionMode.MULTI:
            filenames = [path] if path else ()
        else:
            filenames = path if path else ""
        logger.info("Fell back to console input for path selection")
    finally:
        if root is not None:
            root.destroy()

    if mode == SelectionMode.MULTI:
        if not filenames:
            logger.warning("No images selected in MULTI mode")
            raise SystemExit("No images selected.")
        paths = [Path(f).expanduser() for f in filenames]
        missing = [str(p) for p in paths if not p.is_file()]
        if missing:
            logger.error("Selected image(s) not found: %s", missing)
            raise SystemExit("Selected image(s) not found:\n" + "\n".join(missing))
        logger.info("Selected %d image(s)", len(paths))
        return paths

    if not filenames:
        logger.warning("No image selected in SINGLE mode")
        raise SystemExit("No image selected.")
    path = Path(filenames).expanduser()
    if not path.is_file():
        logger.error("Selected image not found: %s", path)
        raise SystemExit(f"Selected image not found: {path}")
    logger.info("Selected image: %s", path)
    return path
def image_to_data_url(image_path: Path) -> str:
    image_path = image_path.expanduser().resolve()

    if not image_path.is_file():
        logger.error("Image not found: %s", image_path)
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type or not mime_type.startswith("image/"):
        logger.error("Not an image file: %s", image_path)
        raise ValueError(f"Not an image file : {image_path}")

    image_base64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    logger.debug("Converted image to data URL: %s", image_path)
    return f"data:{mime_type};base64,{image_base64}"


def build_image_message(image_path: Path, prompt: str) -> HumanMessage:
    logger.info("Building image message for: %s", image_path)
    return HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}}
        ]
    )