import logging
from pathlib import Path

# Create the logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("audience_pipeline")