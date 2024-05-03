import json
import uuid
import numpy as np
from openai import OpenAI
import streamlit as st
import concurrent.futures

import os
from PyPDF2 import PdfReader

def extract_pdf_content(pdf_path):
    """Extracts text from a single PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")
        return None

def get_pdfs_in_directory(directory):
    """Creates a dictionary of PDF filenames and their content in a directory."""
    pdf_contents = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            content = extract_pdf_content(file_path)
            if content is not None:
                pdf_contents[filename] = content
    return pdf_contents

directory_path = 'data'
pdf_files_content = get_pdfs_in_directory(directory_path)

system_prompt_1 = "Du bist ein konzentrierter und ordentlicher Aufgabenbearbeiter"

system_prompt_2 = "Du bist ein hilfreicher Fragenbeantworter einer Baubehörde, der Fragen basierend auf dem zur Verfügung gestellten Kontext aus behördlicher Sicht beantwortet"

def process_pdf(k, v, question, system_prompt_1, client):
    """
    Processes a PDF document by extracting information relevant to a specified question using GPT model.

    Args:
    k : str
        Key identifying the PDF document.
    v : str
        Content of the PDF document.
    question : str
        Question based on which information is to be extracted.
    system_prompt_1 : str
        Initial prompt for the system.
    client : OpenAI.Client
        Client object to interact with OpenAI API.

    Returns:
    tuple
        A tuple containing the key of the PDF and the model's response.
    """
    prompt = f"Referenzdokument:\n{v}\n\n-----------\n\nBitte extrahiere alle relevanten Informationen aus dem oben genannten Referenzdokument, die zur folgenden Anfrage passen:\n{question}"
    messages = [
        {"role": "system", "content": system_prompt_1},
        {"role": "user", "content": prompt}
    ]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0
    )
    
    return (k, completion)

def execute_processing(pdf_files_content, question, system_prompt_1, client):
    """
    Executes the processing of multiple PDF files concurrently.

    Args:
    pdf_files_content : dict
        A dictionary containing keys and contents of PDF documents.
    question : str
        Question based on which information is to be extracted.
    system_prompt_1 : str
        Initial prompt for the system.
    client : OpenAI.Client
        Client object to interact with OpenAI API.
    """
    responses = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_pdf = {executor.submit(process_pdf, k, v, question, system_prompt_1, client): k for k, v in pdf_files_content.items()}
        for future in concurrent.futures.as_completed(future_to_pdf):
            pdf_key = future_to_pdf[future]
            try:
                response = future.result()
                responses.append(response)
            except Exception as exc:
                print(f'{pdf_key} generated an exception: {exc}')
    return responses