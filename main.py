import gpt_receiver
import window
from file_handler import FileHandler
from tkinter import filedialog
import threading


# updates window api_key outside of window class
# because the GPTReceiver's api_key is updated
# on the <Return> event bound to the api_key_entry.

# the window question_amount is still
# updated inside window class however
def set_api_key(gpt, win):
    win.update_api_key()
    gpt.set_api_key(win.get_api_key())
    win.set_response_text("The API key was updated.")


def create_file_handler():
    # asks user for file, specifies PDF and Text files
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("PDF files", "*.pdf"), ("Text files", "*.txt")),
    )

    # checks for valid file_path
    if not file_path:
        return None

    try:
        return FileHandler(file_path)
    except Exception as e:
        print(f"Error while creating FileHandler: {e}")
        return None


def submit_file(gpt, win):
    file_handler = create_file_handler()

    # checks if there is a file handler object
    if not file_handler:
        win.set_response_text("Error: The file path was invalid.")
        win.file_uploaded = False
        return

    # checks if there are file contents
    if file_handler.get_text() == "":
        win.set_response_text("Error: There were no file contents to upload.")
        win.file_uploaded = False

    # clears GPT history so previous texts/questions don't affect new file question generation
    gpt.clear_message_history()
    win.set_response_text("Uploading file to GPT...")

    # sends  text to GPT, checks if successful
    if not gpt.post_message(f"Remember this text: {file_handler.get_text()} \n\nPlease respond with one word."):
        win.set_response_text("Error: File upload was unsuccessful. " + str(gpt.get_status()))
        win.file_uploaded = False
        return

    win.set_tokens_used_label(gpt.get_response_tokens())
    win.file_uploaded = True

    win.set_response_text("File successfully uploaded.")


def start_submit_file(gpt, win):
    # separate thread for GPT api
    threading.Thread(target=submit_file, args=(gpt, win), daemon=True).start()


def generate_questions(gpt, win):

    # checks if the GPTReceiver has text to work with
    if not win.file_uploaded:
        return

    win.clear_response_text()

    # generates new questions and adds them to the response box
    for i in range(win.get_question_amount()):
        post = gpt.post_message(
            "Write a new study question regarding the text. Please only respond with the question. " +
            "Also be sure that the new question is not a repeat of a previously generated question."
        )
        if post:
            win.add_response_text(str(i + 1) + ". " + gpt.get_response_message() + "\n")
        else:
            win.add_response_text("Error: Could not receive the response.")
            break


def start_generate_questions(gpt, win):
    # separate thread for GPT api
    threading.Thread(target=generate_questions, args=(gpt, win), daemon=True).start()


def setup(gpt, win):
    win.upload_file_button.config(command=lambda: start_submit_file(gpt, win))
    win.generate_button.config(command=lambda: start_generate_questions(gpt, win))
    win.api_key_entry.bind('<Return>', lambda event: set_api_key(gpt, win))
    win.start()


if __name__ == '__main__':
    gpt_receiver = gpt_receiver.GPTReceiver()
    window = window.Window()
    setup(gpt_receiver, window)
