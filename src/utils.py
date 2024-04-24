import os
import sys
import pathlib
import shlex
import subprocess


class Utils:

    # constuctor method
    def __init__(self,env:str,action:str,secret_key:str) -> None:
        self.env = env
        self.action = action
        self.secret_key = secret_key
        self.proj_root_path = f'{pathlib.Path().cwd()}'
        self.secret_key_file_path = f'{self.proj_root_path}/secret_key.txt'
        self.inventrory_path = f'{self.proj_root_path}/inventory/{env}/host_vars'

    # method to decrypt the ansible hostvars files
    def decrypt_hostvars_files(self) -> None:
        try:
            self.create_secret_key_file()
            # decrypt the ansible hostvars files
            host_vars_files = os.listdir(self.inventrory_path)

            for file_name in host_vars_files:
                command = shlex.split(f'ansible-vault decrypt {file_name} --vault-password-file {self.secret_key_file_path}')
                res = subprocess.run(command)
                if not res.returncode:
                    print(f'*** Error: Failed to decrypt the file-{file_name} for env-{self.env} : {res.stderr} ***')
                print(f"*** Success: Successfully decrypted the hostvars file-{file_name} for env={self.env} ***")

        except Exception as e:
            print(f"*** Error: Exception occured wile decrypting the hostvars files for env-{self.env} : {str(e)} ***")

    # method to encrypt the ansible hostvars files
    def encrypt_hostvars_file(self) -> None:
        try:
            self.create_secret_key_file()
            # decrypt the ansible hostvars files
            host_vars_files = os.listdir(self.inventrory_path)

            for file_name in host_vars_files:
                command = shlex.split(
                    f'ansible-vault encrypt {file_name} --vault-password-file {self.secret_key_file_path}')
                res = subprocess.run(command)
                if not res.returncode:
                    print(f'*** Error: Failed to decrypt the file-{file_name} for env-{self.env} : {res.stderr} ***')
                print(f"*** Success: Successfully decrypted the hostvars file-{file_name} for env={self.env} ***")

        except Exception as e:
            print(f"*** Error: Exception occured wile decrypting the hostvars files for env-{self.env} : {str(e)} ***")


    # method to create a secret key file to encrypt & decrypt ansible host_vars files
    def create_secret_key_file(self):
        # removing the old secret_key file
        if os.path.exists(self.secret_key_file_path):
            os.remove(self.secret_key_file_path)

        # create a secret_key files
        with open(self.secret_key_file_path, "w+") as f:
            f.write(self.secret_key)

    # method to invoke the action methods
    def trigger_action(self) -> None:
        if self.action == "encrypt":
            self.encrypt_hostvars_file()
        elif self.action == "decrypt":
            self.decrypt_hostvars_files()
        else:
            print(f'*** Error: Invalid action-{self.action} provided as input ***')

# main starts here...
if __name__ == "__main__":
    try:
        env = sys.argv[1]
        action = sys.argv[2]
        secret_key = sys.argv[3]

        obj = Utils(env,action,secret_key)
        obj.trigger_action()

    except Exception as e:
        print(f"*** Error: Runtime Exception occured while executing the script: {str(e)} ***")