import tkinter as tk


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Study Question Generator")

        self.window_width = 950
        self.window_height = 400
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)

        self.setup_widgets()

        #calss variables
        self.question_amount = 0
        self.previous_entry = ""

    def setup_widgets(self):
        # constant GUI and Stretchability
        # self.root.grid_propagate(False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Response Box
        self.response_text_box = tk.Text(self.root, font=('Calibri', 16), width=80, height=10, padx=15, pady=5,
                                         wrap='word', state='disabled')
        self.response_text_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=tk.S)

        # Response Box scrollBar
        self.scrollbar = tk.Scrollbar(self.root, command=self.response_text_box.yview)
        self.scrollbar.place(in_=self.response_text_box, relx=1.0, rely=-.01, relheight=1.0)
        self.response_text_box.config(yscrollcommand=self.scrollbar.set)

        # question amount entry
        validation = self.root.register(self.question_amount_entry_validation)
        self.question_amount_entry = tk.Entry(self.root, width=5, font=('Calibri', 14), validate='key',
                                              validatecommand=(validation, '%S', '%d'))
        self.question_amount_entry.grid(row=1, column=1, sticky=tk.SW)
        self.question_amount_label = tk.Label(self.root, font=('Calibri', 14, 'bold'), text="Question Amount:")
        self.question_amount_label.grid(row=1, column=0, sticky=tk.SE)

        # API key entry
        self.api_key_entry = tk.Entry(self.root, width=20, font=('Calibri', 14))
        self.api_key_entry.grid(row=0, column=1, sticky=tk.SW)
        self.api_key_label = tk.Label(self.root, font=('Calibri', 14, 'bold'), text="OpenAI API Key:")
        self.api_key_label.grid(row=0, column=0, sticky=tk.SE)

        # extra formatting
        self.blank_1 = tk.Label(self.root, text="\n")
        self.blank_1.grid(row=0, column=2, padx=280)
        self.blank_2 = tk.Label(self.root, text="\n")
        self.blank_2.grid(row=1, column=2, columnspan=3, pady=10)

    def get_question_amount(self):
        return self.question_amount_entry.get()

    def question_amount_entry_validation(self, string, operation):
        
        # checks user backspace (allowed)
        if operation == '0':
            return True

        # checks if user types more than 2 digits (not allowed)
        if len(self.get_question_amount() + string) > 2:
            return False

        # checks if user types non-digit characters (not allowed)
        try:
            int(string)
            return True
        except:
            return False

    def start(self):
        self.root.mainloop()

