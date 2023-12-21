import pathlib
import textwrap
import config
import os
import docx
import fitz  # PyMuPDF for PDF
from comtypes import client

import google.generativeai as genai

# Used to securely store your API key


from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=config.GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

import fitz 
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_text_from_pdf(pdf_path):
    text = []
    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text.append(page.get_text())
    return '\n'.join(text)

def extract_text_from_doc(doc_path):
    word = client.CreateObject('Word.Application')
    doc = word.Documents.Open(doc_path)
    text = doc.Range().Text
    doc.Close()
    word.Quit()
    return text

def extract_text_from_document(document_path):
    _, file_extension = os.path.splitext(document_path)
    if file_extension.lower() == '.docx':
        return extract_text_from_docx(document_path)
    elif file_extension.lower() == '.pdf':
        return extract_text_from_pdf(document_path)
    elif file_extension.lower() == '.doc':
        return extract_text_from_doc(document_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
pdf_path = 'documents\Generated_Contract_20231220122459.docx'
eg = extract_text_from_document(pdf_path)

response = model.generate_content(f'''You are a helpful assistant that gives a long summary of the input text from user in layman language and shows output in bulletin format.
USER: Please provide a clear and straightforward detailed explanation of the text '{eg}' in simple language.Also, could you offer insights from the surrounding text or context that can help users understand how service is meant to be used?
Ensure to highlight any potential pitfalls or attempts at deception related to the usage of service to help users avoid any misunderstandings or misuse. Spot out any traps and loophole in the terms and conditions which can in future harm the person. point out those scenarios .prompt is 
Tone conversational ,spartan, useless corporate jargon
ASSISTANT:''')

# x=to_markdown(response.text)
print(response.text)
# print(x)