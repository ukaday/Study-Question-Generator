import gpt_receiver
import window
import tkinter as tk


def submit_message(gpt, win):

    # check is post is successful
    if not gpt.post_message(win.get_message_text()):
        win.set_response_text("Error:", gpt.get_status()[1])

    # updates UI response box
    win.clear_message_text()
    response_message = gpt.get_response_message()
    if response_message:
        win.set_response_text(response_message)


def setup(gpt, win):
    win.message_text_box.bind('<Alt_L>', lambda event: submit_message(gpt, win))
    win.start()


def main(gpt, win):
    running = True
    while running:
        continue


if __name__ == '__main__':
    gpt_receiver = gpt_receiver.GPTReceiver()
    window = window.Window()
    setup(gpt_receiver, window)
    # main(gpt_receiver, window)
