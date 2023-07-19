import logging.config
import logging.handlers
import json
import os
from anomaly_detection_atom import ad_overlaps_anomaly_detection
from generate_email_alert import generate_email_html, send_notification_email
from datetime import datetime

root_dir1 = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
root_dir2 = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]
root_dir = root_dir1+"\\"+root_dir2
# print(root_dir)
with open(os.path.join(root_dir, "pylogging.json"), "r") as handle:
    logging_config = json.load(handle)
    if "file_handler" in logging_config["handlers"]:
        logging_config["handlers"]["file_handler"]["filename"] = 'Logs/anomaly_detection_' + '{:%Y-%m-%d}.log'.format(
            datetime.now())
    logging.config.dictConfig(logging_config)

logger = logging.getLogger()

def read_config():
    with open('config.json') as file:
        config = json.load(file)
    return config

def main():
    try:
        logger.info("Starting anomaly detection.")

        # Perform anomaly detection
        df, anomaly_detected = ad_overlaps_anomaly_detection(logger=logger)

        logger.info(f"Anomalies detected: {anomaly_detected}")

        if anomaly_detected:
            logger.info("Generating email message.")

            # Generate email message
            msg = generate_email_html(df, logger)

            config = read_config()

            # Email details
            email_to = config['email_to']
            email_from = config['email_from']

            logger.info("Sending notification email.")

            # Send notification email
            send_notification_email(msg, email_to=email_to, email_from=email_from, logger=logger)
        else:
            logger.info('No email alert required')

        logger.info("Anomaly detection completed successfully.")

    except Exception as e:
        # Handle exceptions and perform appropriate error handling/logger
        logger.error(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    # Entry point of the script
    main()
