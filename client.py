import json
import ConfigParser
from client_api import ClientAPI
import sys


def main():
    config_file = sys.argv[1]
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    rec_api = ClientAPI(config)
    rec_api.run()


if __name__ == '__main__':
    main()
