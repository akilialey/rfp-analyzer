from pypdf import PdfReader


def get_pdf_text(path):
    # open the PDF at the given path
    reader = PdfReader(path)

    # make an empty box, then loop through the pages and add each page's text
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"

    # hand the finished text back to whoever called this function
    return all_text


# test it on your RFP
text = get_pdf_text("rfps/rfp.pdf")
print(len(text))