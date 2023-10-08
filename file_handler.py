import PyPDF2 as pypdf


class FileHandler:
    def __init__(self, file_path):

        # class variables
        self.file_path = file_path
        self.file_type = file_path.split(".")[-1].lower()
        self.text = ""

        # checks if file good
        try:
            self.file = open(file_path, 'r')
            self.store_file()
            self.file.close()
        except Exception as e:
            print("Error:", str(e))

    def store_file(self):
        # stores text file
        if self.file_type == "txt":
            self.text += self.file.read()
            return

        # stores pdf file with sentence formatting
        temp_sentence = ""
        for word in self.stream_pdf_file():
            temp_sentence += word + " "

            # checks if word is end of sentence
            if word.find('.'):
                self.text += temp_sentence
                temp_sentence = ""

    def stream_pdf_file(self):
        # streams pdf file word by word
        pdf_reader = pypdf.PdfReader(self.file_path)
        for page in pdf_reader.pages:
            words = page.extract_text().split()
            for word in words:
                yield word


    def get_text(self):
        return self.text
