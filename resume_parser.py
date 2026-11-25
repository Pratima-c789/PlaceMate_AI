import pymupdf


def extract_resume_text(uploaded_file):
    text = ""

    with pymupdf.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    ) as document:

        for page in document:
            text += page.get_text() + "\n"

    return text