from fpdf import FPDF

class PDF(FPDF):

    def header(self):
        self.image("icon.jpg", 10, 8, 25)
        self.set_font("helvetica", "B", 20)
        self.cell(0, 10, "QuickLingoYouTube", border=False, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)

    def write_content(self, title, url,  text):
        text = text.encode('latin-1', 'replace').decode('latin-1')
        title = title.encode('latin-1', 'replace').decode('latin-1')
        url = url.encode('latin-1', 'replace').decode('latin-1')

        text = f"{title}\n" + text
        text = text.split(". ")
        self.set_font("helvetica", 'B', size=13)

        text_to_print = text[0].capitalize()
        self.cell(100, 20, txt=text_to_print)

        self.cell(100, 10, txt=" ")
        self.set_font("helvetica", 'I', size=13)
        for _ in range(2):
            self.ln()
        self.cell(50,5,txt="Youtube Link: "+url,link=url)
        for _ in range(3):
            self.ln()
        for line in text[1:]:
            self.set_font("helvetica", size=13)
            text_to_print = line+'.'
            num_lines = (len(text_to_print) + 89) // 90
            for i in range(num_lines):
                start_index = i * 90
                end_index = min((i + 1) * 90, len(text_to_print))
                line_to_print = text_to_print[start_index:end_index]
                self.cell(100, 5, txt=line_to_print)
                self.ln()

        for _ in range(2):
            self.ln()
        self.set_font("helvetica", 'IU', size=10)
        self.cell(100, 5, txt="Developed By Shakthi",link="https://www.linkedin.com/in/shakthi-s-a0b44a211/")

def make_pdf(title="", url="", text=""):
    pdf = PDF(orientation='P', unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.write_content(title, url, text)
    return pdf
