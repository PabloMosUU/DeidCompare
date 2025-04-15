import json
import pandas as pd
from deduce import Deduce
from deduce.person import Person
from sklearn.metrics import classification_report

INPUT_JSONL = '/media/bigdata/2. Gebruik en toepassing van data/20_12_18_Pablo_Mosteiro_Anonymization/prodigy/texts_namen_met_ano_out/texts_namen_met_ano.jsonl'
OUTPUT_CSV = '/media/pdef/E_ResearchData/2_ResearchData/Ruilin/deduce_patient_result.csv'

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
        predicted_labels.append({(annotation.start_char, annotation.end_char): annotation.tag.upper() for annotation in doc.annotations})

    # Flatten the lists of labels and match predicted labels with true labels based on their positions
    true_labels_flat = [label for sublist in true_labels for label in sublist.items()]
    predicted_labels_flat = [label for sublist in predicted_labels for label in sublist.items()]

    # Sort both lists by positions
    true_labels_flat.sort(key=lambda x: x[0])
    predicted_labels_flat.sort(key=lambda x: x[0])

    # Extract only the label names for the classification report
    true_labels_names = [label[1] if label[1] != 'PATIENT' else 'PERSOON' for label in true_labels_flat]

    # Initialize the new predicted labels list
    predicted_labels_names_matched = []

    # Iterate over true labels
    for true_label in true_labels_flat:
        # Get the position of the true label
        position = true_label[0]

        # Find the predicted label with the same position, if it exists
        predicted_label = next((label for label in predicted_labels_flat if label[0] == position), None)

        if predicted_label is not None:
            # If a predicted label was found, add its name to the new list
            predicted_labels_names_matched.append(predicted_label[1] if predicted_label[1] != 'PATIENT' else 'PERSOON')
        else:
            # If no predicted label was found, add a placeholder to the new list
            predicted_labels_names_matched.append('No Prediction')

    print(true_labels_names)

    # Generate classification report
    report = classification_report(true_labels_names, predicted_labels_names_matched, zero_division=1, output_dict=True)

    # Convert the report to a DataFrame
    report_df = pd.DataFrame(report).transpose()

    # Write the DataFrame to a CSV file with the name 'deduce_result.csv'
    report_df.to_csv(OUTPUT_CSV)
