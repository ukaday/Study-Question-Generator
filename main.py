import gpt_receiver
import window


def submit_message(gpt, win):

    # indicates to user that their request is processing
    win.set_response_text("Streaming Response...")

    # updates gpt api key incase user input new api key in window
    gpt.set_api_key(win.get_api_key())

    # checks if api key has been entered, then updates api keys
    if gpt.openai_api_key == '':
        win.set_response_text("Please enter an API key.")
        return

    # checks if post is successful
    if not gpt.post_message(win.get_message_text()):
        win.set_response_text("Error: " + str(gpt.get_status()[1]))
        return

    # updates UI response box
    win.clear_message_text()
    response_message = gpt.get_response_message()
    if response_message:
        win.set_response_text(response_message)

    # updates UI token display
    win.set_tokens_used_label(gpt.get_response_tokens())


def setup(gpt, win):
    win.message_text_box.bind('<Alt_L>', lambda event: submit_message(gpt, win))
    win.start()


if __name__ == '__main__':
    gpt_receiver = gpt_receiver.GPTReceiver()
    window = window.Window()
    setup(gpt_receiver, window)
