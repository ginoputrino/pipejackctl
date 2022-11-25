from typing import List
from constants import *
import subprocess
from appdirs import *
import os
from configparser import ConfigParser


def _print_std(
    stdout: bytes,
    stderr: bytes,
    # Debug
    verbose: bool = False,
):
    """
    Print terminal output if are different to None and verbose activated
    """

    if stdout is not None and verbose:
        print(f"[_print_std][stdout][type={type(stdout)}]\n{stdout.decode()}")
    if stderr is not None and verbose:
        print(f"[_print_std][stderr][type={type(stderr)}]\n{stderr.decode()}")


def _execute_shell_command(
    command: List[str],
    timeout: int = -1,  # *default= no limit
    # Debug
    verbose: bool = False,
):
    """
    Execute command on terminal via subprocess

    Args:
        - command (str): command line to execute. Example: 'ls -l'
        - timeout (int): (seconds) time to end the terminal process
        - verbose (bool): print variables for debug purposes
    Return:
        - stdout (str): terminal response to the command
        - stderr (str): terminal response to the command
    """
    # Create subprocess
    # NO-RESOURCE-ALLOCATING
    # terminal_subprocess = subprocess.Popen(
    #     command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT  # Example ['ls ','l']
    # )

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT  # Example ['ls ','l']
    ) as terminal_subprocess:
        # Execute command depending or not in timeout
        try:
            if timeout == -1:
                stdout, stderr = terminal_subprocess.communicate()
            else:
                stdout, stderr = terminal_subprocess.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:  # When script finish in time
            terminal_subprocess.kill()
            stdout, stderr = terminal_subprocess.communicate()

        # Print terminal output
        _print_std(stdout, stderr, verbose=verbose)

        # Return terminal output
        return stdout, stderr




def getConfigFileName():
    # in linux ~/.local/share/APP_NAME
    configDir = user_data_dir(APP_NAME, APP_AUTHOR)
    return os.path.join(configDir, CONFIG_FILE)


def createInitialConfig(config):
    config.add_section(CONFIG_SECTION_MAIN)
    config.set(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_LEFT, DEFAULT_LEFT)
    config.set(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_TOP, DEFAULT_TOP)
    config.set(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_WIDTH, DEFAULT_WIDTH)
    config.set(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_HEIGHT, DEFAULT_HEIGHT)
    config.set(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_PWMETACOMMAND, DEFAULT_PW_METACOMMAND )
    config.set(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_PWJACK, DEFAULT_PWJACK )
    config.set(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_MONITOR_FLAGS, DEFAULT_MONITOR_FLAGS)

    config.add_section(CONFIG_SECTION_AUDIO)
    config.set(CONFIG_SECTION_AUDIO, CONFIG_OPTION_AUDIO_DEFAULT_SAMPLE_RATE, DEFAULT_SAMPLE_RATE) 

    config.add_section(CONFIG_SECTION_APPLICATIONS)
    config.set(CONFIG_SECTION_APPLICATIONS, CONFIG_OPTION_APPLICATION_LOCATIONS, DEFAULT_APPLICATIONS)

    configFile = getConfigFileName()
    
    with open(configFile, 'w') as f:
        config.write(f)
    
    return config

def readConfig():
  config = ConfigParser()

  configDir = user_data_dir(APP_NAME, APP_AUTHOR)
  configFile = getConfigFileName()

  if not os.path.exists(configDir):
    os.makedirs(configDir)

  config.read(configFile)

  if (not config.has_section(CONFIG_SECTION_MAIN)):
    createInitialConfig(config)
  
  return config