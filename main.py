import gpt_receiver
import window
from file_handler import FileHandler
from tkinter import filedialog


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


def create_file_object():
    # asks user for file, specifies PDF and Text files
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("PDF files", "*.pdf"), ("Text files", "*.txt"))
    )

    # checks for valid file_path
    if not file_path:
        print("Error: No file path")
        return None

    file_handler = FileHandler(file_path)
    print(file_handler.get_text())


def setup(gpt, win):
    win.upload_file_button.config(command=create_file_object)
    win.start()


if __name__ == '__main__':
    gpt_receiver = gpt_receiver.GPTReceiver()
    window = window.Window()
    setup(gpt_receiver, window)
