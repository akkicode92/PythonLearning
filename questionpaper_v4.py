import pdfplumber
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Check if page_text is not None
                text += page_text + "\n"
    return text.strip()  # Move return statement outside the loop

def extract_key_info(text):
    # Simple extraction logic (this can be improved with NLP libraries)
    key_info = {}

    # Example patterns to extract information
    name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'  # Matches names like "Albert Einstein"
    concept_pattern = r'\bthe\s[a-zA-Z\s]+\b'  # Matches phrases starting with "the"
    location_pattern = r'\b(in|at|to)\s([A-Z][a-z]+)\b'  # Matches locations
    event_pattern = r'\b[a-zA-Z\s]+(event|discovery|theory|phenomenon|activity|reaction)\b'  # Matches events

    # Extracting names
    names = re.findall(name_pattern, text)
    if names:
        key_info['name'] = names[0]  # Take the first name found

    # Extracting concepts
    concepts = re.findall(concept_pattern, text)
    if concepts:
        key_info['concept'] = concepts[0]  # Take the first concept found

    # Extracting locations
    locations = re.findall(location_pattern, text)
    if locations:
        key_info['location'] = locations[0][1]  # Take the location found

    # Extracting events
    events = re.findall(event_pattern, text)
    if events:
        key_info['event'] = events[0]  # Take the first event found

    return key_info

def generate_templates():
    # Example templates
    return [
        "Who is {name}?",
        "What is {concept}?",
        "Where is {location}?",
        "When did {event} happen?",
        "Why did {subject} {action}?",
        "How does {process} work?"
    ]

def generate_questions(text):
    # Extract key information from the text
    key_info = extract_key_info(text)

    # Generate question templates
    templates = generate_templates()

    # Generate questions using the templates
    questions = []
    for template in templates:
        try:
            question = template.format(**key_info)
            questions.append(question)
        except KeyError:
            # Handle missing keys gracefully
            continue
    
    return questions

def main():
    pdf_path = input("Enter the path to the PDF file: ")  # Correct usage of input
    raw_text = extract_text_from_pdf(pdf_path)

    if not raw_text:
        print("No text could be extracted from the document.")
        return

    print("Extracted Text:\n", raw_text)  # Print the extracted text

    # Generate questions based on the extracted text
    generated_questions = generate_questions(raw_text)
    print("\nGenerated Questions:")
    for q in generated_questions:
        print(q)

if __name__ == "__main__":
    main()