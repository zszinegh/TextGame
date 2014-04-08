"""Core module for a text adventure game.

This module is typically run using 'python game.py' but can also be
run as a standalone script the usual way.

The game data file is 'game.json' and expects to be in the same
directory as 'game.py'. Each room is a dictionary record stored in a
master dictionary using the room name as a key. To add more rooms,
duplicate the structure of any room and adjust. I used
'jsoneditoronline.org' to edit this file. The file should make sense
when looking at it in a proper editor.

The main program loop is in 'main_game()' and is ended by setting
'game.player.alive = False'.

Main game methods are in class Game() in 'GameClasses.py'.

"""

import sys
import subprocess
import textwrap

import game_classes


def do_textwrap(text_in, separator=False):
    """Prints wrapped text to console screen.

    Using the imported 'textwrap' module, provides the ability
    to customize console screen output. Set 'width' to the maximum
    screen width (int) desired, and 'text_sep' (str) to the
    character desired between text blocks.

    Args:
        text_in (str): Any string of text.
        separator (bool, optional): True or False determines if
            separator is printed. Default is False.
    """

    # Master setting of text display width.
    # Probably should not go lower than 20, should fit most smartphones.
    width = 40
    # Master text block separator.
    text_sep = '-' * width

    paragraph_list = []

    # This is a hack for displaying the text in multiple paragraphs
    # 'text_in' must have a '<P>' at the splitting point.
    if '<P>' in text_in:
        paragraph_list = text_in.split('<P>')
    else:
        paragraph_list.append(text_in)

    p_len = len(paragraph_list)

    if separator:
        print text_sep
    for paragraph in range(0, p_len):
        textwrap.dedent(paragraph_list[paragraph])
        text_out = textwrap.wrap(paragraph_list[paragraph], width)
        for text in text_out:
            print text
        if paragraph != p_len - 1:
            print  # Paragraph break.
    if separator:
        print text_sep


def clr_screen():
    """Clear console screen."""

    subprocess.call(CLEAR_CMD)


def add_quotes(list_in, title_text):
    """Adds single quotes around items in a list, and a title.

    Makes things like help commands and inventory items stand out
    for the user. Iterates through a list of strings adding single
    quotes around each string.

    Args:
        list_in (list): A list of strings.
        title_text (str): A title that is prefixed to the string.

    Returns:
        text_out (str): The modified text string.
    """

    list_out = []

    for item in list_in:
        item = "'" + item + "'"
        list_out.append(item)

    text_out = ' '.join(list_out)
    text_out = title_text + text_out

    return text_out


def init_game():
    """Initialize the game."""

    # TODO If new game or saved game sets filename.
    # 'game_save.json'
    game.get_db_file('game.json')

    # TODO Will need a room name for where player left off?
    game.load_room('Start')  # Load default 'start' room.

    clr_screen()
    do_textwrap(game.room.description, True)

    entered_name = raw_input('Enter your name ')
    entered_name = entered_name.capitalize()
    game.player.name = entered_name

    clr_screen()
    game.go('start_game')  # Puts player in opening room.
    do_textwrap(game.room.description, True)
    do_textwrap(' '.join(game.user_msg))


def main_game():
    """Start the game loop."""

    # TODO Pull these from a file??
    # The basic commands that can be typed.
    command_list = ['go', 'use', 'inv', 'where', 'look', 'whoami',
                    'help', 'hint', 'quit']

    # Main loop.
    while game.player.alive:
        print
        player_text = raw_input('> ')
        player_text = player_text.lower()
        player_input_list = player_text.split(' ', 1)

        # Clear to make sure nothing leftover from previous use.
        game.user_msg = []

        if player_input_list[0] not in command_list:
            game.user_msg.append("I'm sorry, %s. I'm afraid '%s' is not a"
                                 " valid command." % (game.player.name,
                                                      player_input_list[0]))
            do_textwrap(' '.join(game.user_msg))

        else:
            if player_input_list[0] == 'quit':
                # TODO Question save game?
                print 'Quitting the game...'
                print
                game.player.alive = False

            elif player_input_list[0] == 'help':
                quoted_commands = add_quotes(command_list, 'COMMANDS: ')
                do_textwrap(quoted_commands, True)

            elif player_input_list[0] == 'whoami':
                print 'You are %s.' % game.player.name

            elif player_input_list[0] == 'where':
                print 'You are %s.' % game.room.name_better

            elif player_input_list[0] == 'look':
                clr_screen()
                do_textwrap(game.room.description, True)

            elif player_input_list[0] == 'hint':
                clr_screen()
                do_textwrap(game.room.hint, True)

            elif player_input_list[0] == 'inv':
                quoted_items = add_quotes(game.player.inv_list, 'INVENTORY: ')
                do_textwrap(quoted_items, True)

            elif player_input_list[0] == 'go':
                try:
                    game.go(player_input_list[1])
                except IndexError:
                    print 'go where?'
                else:
                    clr_screen()
                    do_textwrap(game.room.description, True)
                    do_textwrap(' '.join(game.user_msg))

            elif player_input_list[0] == 'use':
                try:
                    game.use(player_input_list[1])
                except IndexError:
                    print 'use what?'
                else:
                    do_textwrap(' '.join(game.user_msg))
            else:
                print 'ERROR: \'%s\' not defined yet.' % player_input_list[0]

    sys.exit(0)

if __name__ == '__main__':

    # Check for windoze for clear screen command.
    if sys.platform.startswith('win32'):
        CLEAR_CMD = 'cls'
    else:
        CLEAR_CMD = 'clear'

    # Instantiate 'game' object.
    game = game_classes.Game()

    # Startup the game.
    init_game()
    main_game()
