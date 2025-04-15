import json
from deduce import Deduce
from deduce.person import Person

INPUT_JSONL = '/media/bigdata/2. Gebruik en toepassing van data/20_12_18_Pablo_Mosteiro_Anonymization/prodigy/texts_namen_met_ano_out/texts_namen_met_ano.jsonl'
OUTPUT_TXT = '/media/pdef/E_ResearchData/2_ResearchData/Ruilin/deduce_errors.txt'

def get_first_names(meta: dict) -> list:
    first_names = f"{meta['VOORNAAM'] if 'VOORNAAM' in meta else ''} {meta['ROEPNAAM'] if 'ROEPNAAM' in meta else ''}"
    return first_names.split()


if __name__ == '__main__':
    # Deduce instance
    deduce = Deduce()

    # Lists to store the texts and true labels
    texts = []
    true_labels = []
    patients = []

    # Load data from the .jsonl file
    with open(INPUT_JSONL, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            texts.append(data['text'])

            # Check if 'spans' key is in data
            if 'spans' in data:
                true_labels.append({(span['start'], span['end']): span['label'] for span in data['spans']})
            else:
                true_labels.append({})

            # Extract patient information
            patient_first_names = get_first_names(data['meta'])
            patient_initial = data['meta']['VOORLETTER']
            patient_surname = data['meta']['ACHTERNAAM']

            # Create a Person instance with the patient's information
            patient = Person(first_names=patient_first_names, initials=patient_initial, surname=patient_surname)

            # Append the patient to the patients list
            patients.append(patient)

    # Store the predicted labels
    predicted_labels = []

    # Deidentify the texts and get the labels
    for text, patient in zip(texts, patients):
        doc = deduce.deidentify(text, metadata={'patient': patient})
        predicted_labels.append({(annotation.start_char, annotation.end_char): (annotation.tag.upper(), doc.text[annotation.start_char:annotation.end_char]) for annotation in doc.annotations})

    # Initialize the file for writing errors
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as output_file:

        # Iterate over the predicted and true labels to find the differences (errors)
        for true, pred, text in zip(true_labels, predicted_labels, texts):
            if true != pred:
                output_file.write(f"Text: {text}\n")
                output_file.write(f"True Label: {true}\n")
                output_file.write(f"Predicted Label: {pred}\n")
                output_file.write("=" * 30 + "\n")
