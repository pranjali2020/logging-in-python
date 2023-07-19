import logging.config
import logging.handlers
import json
import os
from datetime import datetime

root_dir1 = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
root_dir2 = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]
root_dir = root_dir1+"\\"+root_dir2
# print(root_dir)
with open(os.path.join(root_dir, "pylogging.json"), "r") as handle:
    logging_config = json.load(handle)
    if "file_handler" in logging_config["handlers"]:
        logging_config["handlers"]["file_handler"]["filename"] = 'Logs/log_file_' + '{:%Y-%m-%d}.log'.format(
            datetime.now())
    logging.config.dictConfig(logging_config)

logger = logging.getLogger()

def main():
    try:
        logger.info("Starting the main function.")

        a=1
        b=2
        c=a+b
        logger.info(f"Addition of {a} and {b} is {c}")
        logger.info("Main function completed successfully.")

    except Exception as e:
        # Handle exceptions and perform appropriate error handling/logger
        logger.error(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    # Entry point of the script
    main()
