CONFIG_FILE = 'config.ini'
APP_NAME = 'pipejackctl'
APP_AUTHOR = 'aerophyteconsulting.com'
CLOCKRATE_FLAGS = ['-n', 'settings', '0', 'clock.force-rate']
PW_JACK_OPTIONS = ['-p', '1', '-s']

PW_MONITOR_VALUE_SYMBOL = 'value:'

# Configuration Sections

CONFIG_SECTION_MAIN = 'main'
CONFIG_SECTION_AUDIO = 'audio'
CONFIG_SECTION_APPLICATIONS = 'applications'

# Configuration Options

CONFIG_OPTION_MAIN_LEFT = 'left'
CONFIG_OPTION_MAIN_WIDTH = 'width'
CONFIG_OPTION_MAIN_TOP = 'top'
CONFIG_OPTION_MAIN_HEIGHT = 'height'
CONFIG_OPTION_MAIN_PWMETACOMMAND = 'pwmetadatacommand'
CONFIG_OPTION_MAIN_PWJACK = 'pwjackcommand'
CONFIG_OPTION_MAIN_MONITOR_FLAGS = 'monitorflags'

CONFIG_OPTION_AUDIO_DEFAULT_SAMPLE_RATE = 'defaultSamplingRate'

CONFIG_OPTION_APPLICATION_LOCATIONS = 'applicationLocations'


# Configuration Defaults
DEFAULT_LEFT = '10'
DEFAULT_TOP = '10'
DEFAULT_WIDTH = '400'
DEFAULT_HEIGHT = '140'

DEFAULT_PW_METACOMMAND = 'pw-metadata'
DEFAULT_PWJACK= 'pw-jack'
DEFAULT_MONITOR_FLAGS = '-n settings 0 clock.force-rate -m'

DEFAULT_SAMPLE_RATE = '96000'

# Comma separated list of commands
DEFAULT_APPLICATIONS = 'ardour,carla,hydrogen'


MESSAGES_ERROR = {
    "NotImplementedError": "This function is not yet implemented",
    "ValueError": "The value entered is wrong",
}

RECOMMENDED_RATES = [
    8000,
    11025,
    16000,
    22050,
    44100,
    48000,
    88200,
    96000,
    176400,
    192000,
    352800,
    384000,
]
        
CURRENT_SAMPLE_RATE_LABEL ='Current sample rate: '
