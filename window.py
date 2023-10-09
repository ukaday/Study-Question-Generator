import tkinter as tk
import sys


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Study Question Generator")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.window_width = 950
        self.window_height = 400
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(True, True)

        self.setup_widgets()

        # class variables
        self.question_amount = 0
        self.api_key = ""
        self.file_uploaded = False

    def setup_widgets(self):
        # constant GUI and stretchability
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # response box
        self.response_text_box = tk.Text(self.root, font=('Calibre', 14), width=80, height=10, padx=5, pady=5,
                                         wrap='word', state='disabled')
        self.response_text_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=tk.S)

        # response box scroll bar
        self.scrollbar = tk.Scrollbar(self.root, command=self.response_text_box.yview)
        self.scrollbar.place(in_=self.response_text_box, relx=1.0, rely=-.01, relheight=1.0)
        self.response_text_box.config(yscrollcommand=self.scrollbar.set)

        # upload file button
        self.upload_file_button = tk.Button(self.root, text="Upload File", font=('Calibre', 12), height=2, width=15)
        self.upload_file_button.grid(row=0, column=2, padx=200, sticky=tk.S)

        # generate questions button
        self.generate_button = tk.Button(self.root, text="Generate", font=('Calibre', 12), height=2, width=15)
        self.generate_button.grid(row=1, column=2, rowspan=2, pady=10, sticky=tk.S)

        # question amount entry
        validation = self.root.register(self.question_amount_entry_validation)
        self.question_amount_entry = tk.Entry(self.root, width=5, font=('Calibre', 12), validate='key',
                                              validatecommand=(validation, '%S', '%d'))
        self.question_amount_entry.grid(row=1, column=1, sticky=tk.SW)
        self.question_amount_label = tk.Label(self.root, font=('Calibre', 12, 'bold'), text="Question Amount:")
        self.question_amount_label.grid(row=1, column=0, sticky=tk.SE)
        self.question_amount_entry.bind('<Return>', self.set_question_amount)

        # API key entry
        self.api_key_entry = tk.Entry(self.root, width=20, font=('Calibre', 12))
        self.api_key_entry.grid(row=0, column=1, sticky=tk.SW)
        self.api_key_label = tk.Label(self.root, font=('Calibre', 12, 'bold'), text="OpenAI API Key:")
        self.api_key_label.grid(row=0, column=0, sticky=tk.SE)

        # Tokens label
        self.tokens_label = tk.Label(self.root, font=('Calibre', 12, 'bold'), text="Tokens used:")
        self.tokens_label.grid(row=2, column=0, sticky=tk.SE)
        self.tokens_amount_label = tk.Label(self.root, font=('Calibre', 12, 'bold'), text="0")
        self.tokens_amount_label.grid(row=2, column=1, sticky=tk.SW)


        # extra formatting
        # self.blank_1 = tk.Label(self.root, text="\n")
        # self.blank_1.grid(row=0, column=2, padx=280)
        # self.blank_2 = tk.Label(self.root, text="\n")
        # self.blank_2.grid(row=1, column=2, columnspan=3, pady=10)


    def on_close(self):
        sys.exit()

    def set_response_text(self, text):
        # unfreezes text box and replaces text
        self.response_text_box.config(state='normal')
        self.response_text_box.delete("1.0", "end-1c")
        self.response_text_box.insert(tk.END, text)
        self.response_text_box.config(state='disabled')
        self.root.update_idletasks()

    def add_response_text(self, text):
        # unfreezes text box and adds to existing text
        self.response_text_box.config(state='normal')
        self.response_text_box.insert(tk.END, text)
        self.response_text_box.config(state='disabled')
        self.root.update_idletasks()

    def clear_response_text(self):
        # clears text box
        self.response_text_box.config(state='normal')
        self.response_text_box.delete("1.0", "end-1c")
        self.response_text_box.config(state='disabled')

    def set_question_amount(self, event):
        value = self.question_amount_entry.get()

        # checks if entry is empty
        if value != "":
            self.question_amount = int(value)
            self.set_response_text("Question amount was updated.")

            # clears entry
            self.question_amount_entry.delete(0, tk.END)
            return

        self.set_response_text("Question amount could not be updated.")

    def get_question_amount(self):
        return self.question_amount

    def question_amount_entry_validation(self, string, operation):

        # checks user backspace (allowed)
        if operation == '0':
            return True

        # checks if user types more than 2 digits (not allowed)
        if len(self.question_amount_entry.get() + string) > 2:
            return False

        # checks if user types non-digit characters (not allowed)
        try:
            int(string)
            return True
        except:
            return False

    def update_api_key(self):
        value = self.api_key_entry.get()

        # checks if entry is empty
        if value != "":
            self.api_key = value

        # clears entry
        self.api_key_entry.delete(0, tk.END)

    def get_api_key(self):
        return self.api_key

    def set_tokens_used_label(self, tokens):
        self.tokens_amount_label.config(text=str(tokens))
        self.root.update_idletasks()

    def start(self):
        self.root.mainloop()

