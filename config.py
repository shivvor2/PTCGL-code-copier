from pynput import keyboard

BATCH_SIZE = 10 # PTCGL only supports 10 codes per redeem on9

KEY_NEXT_BATCH = keyboard.Key.space
KEY_PREV_BATCH = "s"
KEY_FORWARD = "w"
KEY_BACKWARD = "q"
KEY_LOCK = "r"
KEY_EXIT = keyboard.Key.esc