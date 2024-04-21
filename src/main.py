import pathlib
import sys
import shlex
import subprocess
from typing import List


class MernTasksApp:
    def __init__(self,env: str ,action: str) -> None:
        self.action = action
        self.env = env
        self.__container_name = 'mern-tasks-app'
        self.__proj_root_path = f'''{pathlib.Path().cwd()}'''
        self.__inventory_path = f'{self.__proj_root_path}/inventory/{self.env}/hosts'


    # method to deploy the MERN Tasks App Container in AWS Infra
    def __deploy_container(self) -> None:
        try:
            playbook_path = f'{self.__proj_root_path}/playbooks/deploy-container.yaml'
            play_command = shlex.split(f'ansible-playbook -i {self.__inventory_path} {playbook_path}')
            
            print(f'*** Info: The playbook to deploy the container is started in env - {self.env} ***')

            res = subprocess.run(play_command)

            if res.returncode:
                print(f'*** Error: Playbook to deploy the container is failed in env - {self.env} : {str(res.stderr)} ***',file=sys.stderr)

            print(f'*** Success: The playbook to deploy the container is successfully completd ***')

        except Exception as e:
            print(f'*** Error: Exception occured while pulling and running the container in env - {self.env} : {str(e)} ***')

    # method to fetch the running container information from AWS Infra
    def __fetch_container_info(self) -> None:
        try:
            playbook_path = f'{self.__proj_root_path}/playbooks/fetch-container-info.yaml'
            play_command = shlex.split(f'ansible-playbook -i {self.__inventory_path} {playbook_path}')

            print(f'*** Info: The playbook to fetch the container info in env - {self.env} ***')

            res = subprocess.run(play_command)

            if res.returncode:
                print(f'*** Error: Playbook to fetch the container info running in AWS infra is failed for env - {self.env} : {str(res.stderr)} ***', file=sys.stderr)

            print(f'*** Success: The playbook to fetch the container info running in AWS Infra is successfully completd ***')

        except Exception as e:
            print(f'*** Error: Exception occured while to fetch the container info running in AWS Infra for env - {self.env} : {str(e)} ***')

    # method to stop the running containers
    def __stop_container(self) -> None:
        try:
            playbook_path = f'{self.__proj_root_path}/playbooks/stop-container.yaml'
            play_command = shlex.split(f'ansible-playbook -i {self.__inventory_path} {playbook_path}')

            print(f'*** Info: The playbook to stop the container is started for env - {self.env} ***')

            res = subprocess.run(play_command)

            if res.returncode:
                print(f'*** Error: Playbook to stop the container is failed in env - {self.env} : {str(res.stderr)} ***', file=sys.stderr)

            print(f'*** Success: The playbook to stop the container is successfully completd ***')

        except Exception as e:
            print(f'*** Error: Exception occured while stopping the container for env - {self.env} : {str(e)} ***')

    # public access method to trigger the respsction private method based on action
    def perform_action(self) -> None:
        if self.action == 'info':
            self.__fetch_container_info()
        elif self.action == 'deploy':
            self.__deploy_container()
        elif self.action == 'stop':
            self.__stop_container()
        else:
            print(f'*** Error: Invalid action - {self.action} provided as input ***',file=sys.stderr)

if __name__ == "__main__":
    try:
        # mapping the commandline args
        env = sys.argv[1]
        action = sys.argv[2]

        obj = MernTasksApp(env,action)
        obj.perform_action()

    except Exception as e:
        print(f"*** Error: Something went wrong while performing the action - {action} : {str(e)} ***",file=sys.stderr)
