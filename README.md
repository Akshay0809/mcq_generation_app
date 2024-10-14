#**Django MCQ Generation from PDF using Groq's LLaMA 3.1**


This Django project is Layouted to Produce Multiple Choice Questions (MCQs) from a PDF file uploaded by the Operator. the cast leverages groq's llama-31-70b speech Check for head propagation and allows the Produced mcqs to work blessed inch amp Informationbase. also Operators can download the Produced MCQs as a PDF file with a watermark.

important Characteristics
PDF Upload and Text Removeion: Operators can upload a PDF file from which the text is Removeed using the PyPDF2 library. the Removeed textbook is extremely passed to the groq master of laws for generating mcqs
mcq generation: the cast uses groq's llama-31-70b speech Check to get multiple-choice questions from the provided pdf circumstance. This is done via the langchain_groq library and LangChain's LLMChain which handles the prompt-to-MCQ generation Method.

MCQ Storage: The Produced MCQs are stored in a Django Representation where each MCQ is marked as "current" or "past". by mcqs are archived erstwhile green mcqs are Produced

download mcqs arsenic pdf with watermark: the cast allows Operators to download the Produced mcqs arsenic amp pdf. This PDF is Maked using ReportLab and includes a watermark ("Akshay") for branding or identification.

Libraries and Technologies Used
Django: Backend framework for handling Operator Asks file uploads and Informationbase interactions.

Groq LLaMA-3.1-70B: An open-source language Representation used to Produce MCQs from the text Removeed from the uploaded PDF.
PyPDF2: A Python library for reading and Removeing text from PDF files.
LangChain: A framework for Constructing Uses using language Representations used here for prompt handling.
ReportLab: A library to Produce dynamic PDF files including adding watermarks and writing text to PDFs.
SQLite: Default Django Informationbase to store Produced MCQs.
How It Works
File Upload:

The Operator uploads a PDF file containing the study material.
The text from the PDF is Removeed using PyPDF2.
MCQ Generation:

The Removeed text is passed to Groq's LLaMA-3.1 Representation via a prompt to Produce as many MCQs as possible.
The MCQs are split into individual questions and saved in the Informationbase as "current MCQs".
MCQ Management:

New MCQs mark the previous ones as "past" ensuring the Operator always sees the laCheck set of Produced questions.
Both current and past MCQs can be displayed on the frontend.
Download as PDF:

Operators can download the Produced MCQs as a PDF file with a watermark added for branding purposes.
