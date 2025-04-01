import logging
import os
import asyncio
import time
import shutil
from factory import Factory
from tools import load_config, init_logger
from drivers.driver_mega import DriverMega
from drivers.driver_mysql import DriverMysql
import psutil

def flush_temp_folder(temp_dir):
    """Delete all files in the temp directory."""
    try:
        # Check if the temp directory exists
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            # Iterate through all files in the temp directory
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)  # Delete file
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Delete directory
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            print(f"All files in {temp_dir} have been deleted.")
        else:
            print(f"The folder {temp_dir} does not exist.")
    except Exception as e:
        print(f"Error flushing the temp folder: {e}")

async def get_database_name(default_name):
    """Prompt user for a database name asynchronously."""
    return input(f"Enter database name (default: {default_name}): ").strip() or default_name

async def main():
    try:
        config = load_config()
        init_logger('logs/restoration.log')
        logger = logging.getLogger('clouddump')

        # Get user-defined or default database name
        database_name = await get_database_name(config['database']['name'])

        # Initialize Mega service
        service = Factory().create(config['service']['driver'], config['service'])
        mega_client = DriverMega(config['service'])

        # Fetch latest backup file
        logger.info("Fetching latest backup file from Mega...")
        files = mega_client._get_folder_files()
        if not files:
            logger.error("No backup files found on Mega.")
            return

        latest_file_id, latest_file_metadata = max(files.items(), key=lambda x: x[1]['ts'])
        latest_file_name = latest_file_metadata['a']['n']
        print(f"Latest backup file: {latest_file_name}")

        # Find the file
        file = mega_client.mega.find(latest_file_name)
        if not file:
            logger.error("Failed to retrieve download file.")
            return

        # Define a temp directory and ensure it exists
        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Define the full path for the downloaded file
        temp_file_path = os.path.join(temp_dir, latest_file_name)
        final_file_path = temp_file_path + "_ready.sql"

        try:
            logger.info(f"Downloading backup file to: {temp_file_path}")
            mega_client.mega.download(file, temp_dir)

            logger.info("Download completed. Now checking file accessibility...")
        except Exception as e:
            logger.error(f"Error during file download: {e}")
            return  # Exit early if the download fails


        # Wait for file release
        logger.info(f"Downloaded file saved as: {final_file_path}")

        # Restore to MySQL
        mysql_client = DriverMysql(config['database'])
        logger.info("Restoring database...")
        await asyncio.to_thread(mysql_client.dump, database_name, final_file_path)

        logger.info("Database restoration completed successfully.")

        # Delete the temporary file
        flush_temp_folder(temp_dir)
        logger.info(f"Temporary file {final_file_path} deleted.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
