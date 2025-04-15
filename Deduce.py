import json
import pandas as pd
from deduce import Deduce
from sklearn.metrics import classification_report

# Deduce instance
deduce = Deduce()

# Lists to store the texts and true labels
texts = []
true_labels = []

# Load data from the .jsonl file
with open('/media/bigdata/2. Gebruik en toepassing van data/20_12_18_Pablo_Mosteiro_Anonymization/prodigy/texts_namen_met_ano_out/texts_namen_met_ano.jsonl', 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        texts.append(data['text'])
        if 'spans' in data:
            true_labels.append({(span['start'], span['end']): span['label'] for span in data['spans']})
        else:
            true_labels.append({})

# Store the predicted labels
predicted_labels = []

# Deidentify the texts and get the labels
for text in texts:
    doc = deduce.deidentify(text)
    predicted_labels.append({(annotation.start_char, annotation.end_char): annotation.tag.upper() for annotation in doc.annotations})

# Flatten the lists of labels and match predicted labels with true labels based on their positions
true_labels_flat = [label for sublist in true_labels for label in sublist.items()]
predicted_labels_flat = [label for sublist in predicted_labels for label in sublist.items()]

# Sort both lists by positions
true_labels_flat.sort(key=lambda x: x[0])
predicted_labels_flat.sort(key=lambda x: x[0])

# Extract only the label names for the classification report
true_labels_names = [label[1] for label in true_labels_flat]

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
        predicted_labels_names_matched.append(predicted_label[1])
    else:
        # If no predicted label was found, add a placeholder to the new list
        predicted_labels_names_matched.append('No Prediction')

# Generate classification report
report = classification_report(true_labels_names, predicted_labels_names_matched, zero_division=1, output_dict=True)

# Convert the report to a DataFrame
report_df = pd.DataFrame(report).transpose()

# Write the DataFrame to a CSV file with the name 'deduce_result.csv'
report_df.to_csv('/media/pdef/E_ResearchData/2_ResearchData/Ruilin/deduce_result.csv')
