from util import *
from config import *

# States
state_tracker = StateTracker(0,0,False) # Yes this is very stupid

code_list = get_all_code("codes.txt")
code_batches = [code_list[x: x + BATCH_SIZE] for x in range(0, len(code_list), BATCH_SIZE)]

# # shorthand (cuz Im lazy)
# def action(action):
#     move(code_batches, state_tracker, action)

get_current_code(code_batches, state_tracker)

# with keyboard.GlobalHotKeys({
#         KEY_NEXT_BATCH: lambda: move(code_batches,state_tracker, "next_batch"), 
#         KEY_PREV_BATCH: lambda: move(code_batches,state_tracker, "prev_batch"),
#         "<ctrl>+v": lambda: move(code_batches,state_tracker, "forward"),
#         KEY_FORWARD: lambda: move(code_batches,state_tracker, "forward"),
#         KEY_BACKWARD: lambda: move(code_batches,state_tracker, "backward"),
#         KEY_LOCK: lambda: lock(state_tracker),
#         KEY_EXIT: quit}) as listener:
#     try:
#         listener.join()
#     except KeyboardInterrupt:
#         print(f"Redeemed {state_tracker.current_batch_index + 1} out of {len(code_batches)} batches")
#         print("Exiting script")  

# Collect events until released
with keyboard.Listener(on_press = lambda key: on_press(key, code_batches, state_tracker), on_release = lambda key: on_release(key, code_batches, state_tracker)) as listener:
    listener.join()

input("Press any key to continue...")