"""Classes module for TextGame"""


import json


class Game(object):
    """Main game class."""

    def __init__(self):
        """Init method."""

        self.room = Room()  # To access room attributes from this object.
        self.player = Player()  # To access player attributes.

        self.json_db = {}  # Stores game data from json file as dict.

        # Stores current room name for use in 'use' method.
        self.current_room = ''

        # Use for player response messages, not program errors.
        self.user_msg = []  # List so we can do ' '.join().

    def get_db_file(self, filename):
        """Load a json game data file from disk.

        Args:
            filename (str): Name of json file.
        """

        try:
            with open(filename, 'r') as f_in:
                try:
                    self.json_db = json.load(f_in)
                except ValueError as error:
                    print 'JSON error: %s' % error

        except IOError as error:
            print 'File error: %s' % error

    # TODO What happens if json doesnt load???

    def load_room(self, room_name, update_inv=True):
        """Load room data from dict, called as needed.

        Args:
            room_name (str): Name of room to load.
            update_inv (bool, optional): True or False determines
                if inventory is updated. Set to false if just reloading
                a room. Default is True.
        """

        self.current_room = room_name  # Store the current room.

        try:
            self.json_db[room_name]
        except KeyError:
            # This shouldn't happen if all rooms are defined in
            # 'game.json'.
            print 'Room %s not available yet.' % room_name
            # 'clr_screen()' would prevent message being seen.
            raw_input('DEBUG: Press ENTER to continue.')
        else:
            self.room.room_record = self.json_db[room_name]

        # Load room information.
        self.room.name = self.room.room_record['name']
        self.room.name_better = self.room.room_record['name_better']

        self.room.description = self.room.room_record['description']
        self.room.adjacent_rooms = self.room.room_record['adjacent_rooms']
        self.room.hint = self.room.room_record['hint']

        # Check to see if player entered a 'Dead' room.
        if self.room.name == 'Dead':
            self.player.alive = False
        else:
            pass  # Player still alive.

        # Update player's inventory with items found in room.
        if update_inv:
            for item in self.room.room_record['items']:
                if item not in self.player.inv_list:
                    self.player.inv_list.append(item)
                    self.user_msg.append('\'%s\' added to inventory.' % item)
                else:
                    pass  # Item already there.
        else:
            pass  # When just reloading room.

    def go(self, room_command):
        """Executes the room changes.

        Validates what the player entered for a command to go to an
        adjacent room and calls 'load_room()' method.

        Args:
            room_command (str): Second part of user entered 'go'
            command.
        """

        if room_command in self.room.adjacent_rooms:
            self.load_room(self.room.adjacent_rooms[room_command])

        else:
            self.user_msg.append("I'm sorry, %s. I'm afraid you "
                                 "can't go there." % self.player.name)

    def use(self, inv_item):
        """Allows player to use their inventory items.

        If the valid inventory item is also 'usable' in the current
        room, this method will copy updated details to
        'room.room_record'.

        Args:
            inv_item (str): An inventory item.
        """

        # Clear to make sure nothing leftover.
        self.user_msg = []

        # If usable item in the room, that triggers update.
        if inv_item in self.player.inv_list:
            if inv_item in self.room.room_record['usable_items']:

                self.room.room_record['description'] = self.room.room_record[
                    'description_unlocked']
                self.room.room_record['adjacent_rooms'] = \
                    self.room.room_record['adjacent_rooms_unlocked']

                self.load_room(self.current_room, False)

                self.user_msg.append(self.room.room_record[
                    'usable_items'][inv_item])

            else:
                self.user_msg.append("I'm sorry, %s. I'm afraid you "
                                     "can't use your '%s' here" %
                                     (self.player.name, inv_item))

        else:
            self.user_msg.append("I'm sorry, %s. I'm afraid you "
                                 "can't do that." % self.player.name)


class Player(object):
    """Defines the player."""

    def __init__(self):
        """Init method."""

        self.name = ''  # Name of player.
        self.inv_list = []  # Stores a list of inventory items.

        self.alive = True  # Is the player still alive?


class Room(object):
    """Defines the room."""

    def __init__(self):
        """Init method."""

        self.room_record = {}  # Dict to store the record of a room.

        self.name = 'room name'  # Name of room.
        # So when the user types 'where', the grammar is correct.
        self.name_better = 'more grammatically correct name'

        self.description = 'room description'  # Description of room.
        self.adjacent_rooms = {}  # Dict to store connected rooms.
        self.hint = 'room hint'  # Stores a hint for a room.
