import json
import re
import itertools
from pathlib import Path

# Define the cleaning function
def clean_text(text):
    # Remove filler words
    filler_words = ['uh', 'um', 'like']
    text_words = text.split()
    cleaned_text = ' '.join([word for word in text_words if word.lower() not in filler_words])

    # Normalize text
    cleaned_text = cleaned_text.lower()

    # Remove unnecessary punctuation
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)

    # Remove repetitions (this is quite complex and would normally be done with some form of natural language analysis, we will just remove adjacent repeated words for this demo)
    cleaned_text = ' '.join(word for word, _ in itertools.groupby(cleaned_text.split()))

    return cleaned_text

# Define the transcript processing function
def process_transcript(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Structure the transcript
    dialogue = []
    current_sequence = None
    current_timestamp = None
    current_text = []
    for line in lines:
        line = line.strip()
        if line.isdigit():  # This is a sequence number
            # If we have text currently being processed, save it before continuing
            if current_sequence and current_timestamp and current_text:
                dialogue.append({
                    'sequence': current_sequence,
                    'timestamp': current_timestamp,
                    'text': clean_text(" ".join(current_text)),
                })
            current_sequence = line
            current_text = []
        elif "-->" in line:  # This is a timestamp
            current_timestamp = line
        elif line:
            current_text.append(line)

    # Don't forget to save the last dialogue segment if the file does not end with a blank line
    if current_sequence and current_timestamp and current_text:
        dialogue.append({
            'sequence': current_sequence,
            'timestamp': current_timestamp,
            'text': clean_text(" ".join(current_text)),
        })

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as out_file:
        json.dump(dialogue, out_file, ensure_ascii=False, indent=4)

# Chemin relatif pour le fichier d'entrée et de sortie
current_directory = Path(__file__).parent
input_file_path = current_directory / 'mark_interview.txt'
output_file_path = current_directory / 'cleaned_transcript.json'


process_transcript(input_file_path, output_file_path)


