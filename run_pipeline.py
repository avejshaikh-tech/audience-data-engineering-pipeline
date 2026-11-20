import subprocess
import sys
import logging
from pathlib import Path

# Find the project directory
BASE_DIR = Path(__file__).resolve().parent

# Create logging directory
(BASE_DIR / "logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename=BASE_DIR / "logs" / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("pipeline_runner")

# Pipeline steps in execution order
steps = [
    "src/ingest.py",
    "src/load.py",
    "src/transform.py"
]

def run_pipeline():
    logger.info("Pipeline started")

    for step in steps:
        print(f"\nRunning: {step}")
        logger.info("Starting step: %s", step)

        try:
            subprocess.run(
                [sys.executable, str(BASE_DIR / step)],
                cwd=BASE_DIR,
                check=True
            )

            logger.info("Completed step: %s", step)

        except subprocess.CalledProcessError:
            logger.exception("Pipeline failed at step: %s", step)
            print(f"Pipeline failed at: {step}")
            raise

    logger.info("Pipeline completed successfully")
    print("\nEND-TO-END PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_pipeline()