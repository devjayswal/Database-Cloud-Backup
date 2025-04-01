import subprocess
import os
import sys
import logging
import errno

class DriverMysql:
    def __init__(self, params):
        self.user_name = params['user_name']
        self.password = params['password']
        self.host = params['host'].split(":")[0]  # Extract only the hostname
        self.port = 3306 if 'port' not in params else params['port']
        self.logger = logging.getLogger('clouddump')

    def dump(self, database_name, file_name=None):
        try:
            file_name = f"{file_name}.sql"

            self.logger.info(f"Dumping {database_name} to {file_name}...")

            # Define the path to mysqldump.exe
            mysqldump_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

            # Open the file in write mode
            with open(file_name, "w") as output_file:
                retcode = subprocess.call(
                    [
                        mysqldump_path,
                        "-u", self.user_name,
                        f"-p{self.password}",  # No space after `-p`
                        "-h", self.host,
                        "-P", str(self.port),
                        "--opt",
                        database_name
                    ],
                    stdout=output_file,  # Redirect output
                    stderr=subprocess.PIPE,
                    shell=False  # Avoid security risks
                )

            if retcode == 127:
                self.logger.critical("mysqldump not found. Ensure it is installed and in PATH.")
                sys.exit(errno.ENOPKG)
            elif retcode == 2:
                self.logger.critical("Wrong MySQL user and/or password.")
                sys.exit(errno.EPERM)
            elif retcode != 0:
                print(f"mysqldump failed with error code: {retcode}")
                sys.exit(1)

            return file_name  # Return the dumped file

        except OSError as e:
            print(f"Execution failed: {e}")
