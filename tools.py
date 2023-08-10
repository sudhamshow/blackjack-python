import sys
import time


def readch():
    """
    This function is for handling raw character based on the operating system
    being used. This was referenced from StackOverflow
    :return: character input object if OS is Windows
    """
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty

    def _getch():
        """
        This function facilitates asynchronous single character input on
        POSIX based systems.
        :return: (string) Returns the read raw character
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch()


def validate_input(valid_args,
                   welcome_message="What would you like to do?",
                   error_message=" is not a valid input, please try again\n",
                   ):
    """
    This function reads a single key press, and if it is among the accepted
    values, the read input is returned else, user is prompted to enter valid
    values again.
    :param valid_args: list of valid characters, within which the user input
    should be
    :param welcome_message: (string) Message prompted at the beginning of
    user input
    :param error_message: (string) Message prompted if read input is not
    among valid_args
    :return: (string) read input which is among valid_args
    """
    time.sleep(0.5)
    print(welcome_message)
    while True:
        read_value = readch()
        if str.lower(read_value) in valid_args:
            clear_prev_lines(1)
            time.sleep(0.5)
            break
        else:
            clear_prev_lines(1)
            time.sleep(0.5)
            print(read_value + error_message)
            sys.stdout.flush()
    return read_value


def move_lines_up(num_lines=0):
    """
    This function moves the cursor up by num_lines on the terminal
    :param num_lines: (int) The number of lines the cursor has to move up by
    :return: None
    """
    print("\r", end="")
    for line in range(num_lines):
        print("\033[F", end="")


def move_lines_down(num_lines=0):
    """
    This function moves the cursor down by num_lines on the terminal
    :param num_lines: (int) The number of lines the cursor has to move down by
    :return: None
    """
    print("\r", end="")
    for line in range(num_lines):
        print("\033[E", end="")


def clear_prev_lines(num_lines=0):
    """
    This function clears the required number of previous lines relative to
    the current position of the cursor
    :param num_lines: (int) the number of lines above the current cursor
    position that has to be cleared
    :return: None
    """
    for line in range(num_lines):
        print("\033[F", end="")
        print("\033[2K", end="")


def overwrite_prev_line(player, position, jump_space=0):
    """
    This function overwrites a previous line with delay for perceivable
    terminal transition
    :param player: The object whose representation is being printed (Player
    object)
    :param position: The line above the jump_space which has to be
    overwritten for animated transition effects
    :param jump_space: The initial buffer length beyond which position is
    counted
    :return: None
    """
    print("\033[" + str(position + jump_space) + "F", end="")
    print("\033[2K", end="")
    time.sleep(0.5)
    print(player, end="")
    sys.stdout.flush()
    print("\033[" + str(position + jump_space) + "E", end="")


def update_current_line(item):
    """
    This function updates the current line with a delay for animated
    transition on the terminal
    :param item: Object that needs to be printed
    :return: None
    """
    print(item, end="\r")
    time.sleep(1)
    sys.stdout.write("\033[2K")


def clear_screen():
    """
    This function clears the entire terminal
    :return: None
    """
    print("\033[2J")
    print('\033[H')
