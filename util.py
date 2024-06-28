import pyperclip
from pynput import keyboard
from dataclasses import dataclass
from config import *
import os

# This is stupid, if only python has referencing
@dataclass
class StateTracker:
    current_batch_index: int
    current_item_index: int
    locked: bool

def get_all_code(txt_name) -> list[str]:
    file = open(txt_name, "r")
    code_list = []
    for line in file:
        thisline = line.strip()
        if len(thisline): # Check for not empty
            code_list.append(thisline)
    return code_list

def get_current_code(code_batches, state_tracker: StateTracker) -> None:
    pyperclip.copy(code_batches[state_tracker.current_batch_index][state_tracker.current_item_index])
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Copied code {state_tracker.current_item_index+1}/{len(code_batches[state_tracker.current_batch_index])} for batch {state_tracker.current_batch_index+1}/{len(code_batches)}")

def move(code_batches, state_tracker: StateTracker, action) -> None:
    if state_tracker.locked:
        # print("Script locked, no action permitted")
        return
    match action:
        case "next_batch":
            if state_tracker.current_batch_index == len(code_batches)-1:
                print("Already at last batch")
            else:
                state_tracker.current_batch_index += 1
                state_tracker.current_item_index = 0
        case "prev_batch":
            if state_tracker.current_batch_index == 0:
                print("Already at first batch")
            else:
                state_tracker.current_batch_index -= 1
                state_tracker.current_item_index = 0
        case "forward":
            state_tracker.current_item_index = (state_tracker.current_item_index + 1) % len(code_batches[state_tracker.current_batch_index]) # To deal with case when total amount of keys is not multiple of batch_size
        case "backward":
            state_tracker.current_item_index = (state_tracker.current_item_index - 1) % len(code_batches[state_tracker.current_batch_index])
    get_current_code(code_batches, state_tracker)

def lock(state_tracker: StateTracker) -> None:
    state_tracker.locked = not state_tracker.locked
    print("Locked the code copier" if state_tracker.locked else "Unlocked the code copier")

def listen(key, target) -> bool:
    if isinstance(target, str):
        return hasattr(key, 'char') and key.char == target
    elif isinstance(target, keyboard.Key):
        return key == target
    else:
        return False

def on_press(key, code_batches, state_tracker):
    if key == keyboard.Key.ctrl_l: # Ctrl + V, hard code brrrrr
        if keyboard.Controller().pressed(keyboard.KeyCode.from_char('v')):
            move(code_batches, state_tracker, "forward")
    elif listen(key, KEY_FORWARD):
        move(code_batches, state_tracker, "forward")
    elif listen(key, KEY_BACKWARD):
        move(code_batches, state_tracker, "backward")
    elif listen(key, KEY_NEXT_BATCH):
        move(code_batches, state_tracker, "next_batch")
    elif listen(key, KEY_PREV_BATCH):
        move(code_batches, state_tracker, "prev_batch")
    elif listen(key, KEY_LOCK):
        lock(state_tracker)
    

def on_release(key, code_batches, state_tracker):
    if listen(key, KEY_EXIT):
        # Stop listener
        print(f"Redeemed {state_tracker.current_batch_index} out of {len(code_batches)} batches")
        return False