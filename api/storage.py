'''This api module safely stores data given to it by modules. This data
will not be lost of the bot shuts down and should be properly saved,
even if the bot crashes.
Data for this module is stored in ~/.BBot/storage/.
'''
import os
import json

# Variables
STORAGE_PATH = os.path.join(os.path.expanduser('~'),
                            '.BBot', 'storage', '')
registered = {}

# Functions
def register(network, module):
    # Check if database exists, create if missing
    if network in registered:
        if module not in registered[network]:
            registered[network][module] = Database()
    else:
        registered[network] = {
            module: Database()
        }

    # Return the database
    return registered[network][module]

def load():
    '''Load databases from ~/.BBot/storage/.'''
    for storagepath in os.listdir(STORAGE_PATH):
        network = storagepath.replace('.json', '')
        registered[network] = json.load(file(STORAGE_PATH + storagepath))

def save():
    '''Save the databases in a file with the name of the network.'''
    for network in registered:
        filename = network + '.json'
        json.dump(registered[network], file(STORAGE_PATH + filename, 'w'))
