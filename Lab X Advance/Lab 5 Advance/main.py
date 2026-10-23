# main.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_parser import ConfigParser
from communication_agent import CommunicationAgent
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

def main():
    base_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(base_dir, 'configs', 'comm_pipeline_config.json')

    try:
        ensure_directory_exists(os.path.join(base_dir, 'data', 'reports'))
        ensure_directory_exists(os.path.join(base_dir, 'data', 'incoming_attachments'))
        ensure_directory_exists(os.path.join(base_dir, 'reports'))

        logger.info(f"Loading configuration from: {config_file_path}")
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()

        logger.info("Initializing Communication Agent...")
        agent = CommunicationAgent(config, base_dir)

        logger.info("Running Communication Agent workflow...")
        agent.run()
        logger.info("Communication automation process completed.")

    except ValueError as e:
        # กรณีที่พบบ่อยที่สุดคือยังไม่ได้ตั้งค่าไฟล์ .env
        # แจ้งให้ชัดเจนแทนการโยน traceback ดิบใส่ผู้ใช้
        logger.critical(f"Configuration error: {e}")
        logger.info("กรุณาคัดลอก .env.example เป็น .env แล้วกรอกค่าให้ครบก่อนรันอีกครั้ง")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.critical(f"File not found: {e}")
        logger.info("ตรวจสอบว่าไฟล์ config และไฟล์แนบที่ระบุไว้มีอยู่จริง")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
