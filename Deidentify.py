import json
import pandas as pd
from deidentify.base import Document
from deidentify.taggers import FlairTagger
from deidentify.tokenizer import TokenizerFactory
from sklearn.metrics import classification_report
from deidentify.base import Annotation

# Create a mapping dictionary
tag_mapping = {
    'Internal_Location': 'LOCATIE', 
    'Age': 'LEEFTIJD', 
    'Phone_fax': 'TELEFOONNUMMER', 
    'Name': 'PERSOON', 
    'SSN': 'PATIENTNUMMER', 
    'Hospital': 'INSTELLING', 
    'Email': 'URL', 
    'Initials': 'PERSOON', 
    'Organization_Company': 'INSTELLING', 
    'ID': 'PATIENTNUMMER', 
    'Care_Institute': 'INSTELLING', 
    'Date': 'DATUM', 
    'URL_IP': 'URL', 
    'Address': 'LOCATIE'
}

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

# Select downloaded model
model = 'model_bilstmcrf_ons_fast-v0.2.0'

# Instantiate tokenizer
tokenizer = TokenizerFactory().tokenizer(corpus='ons', disable=("tagger", "ner"))

# Load tagger with a downloaded model file and tokenizer
tagger = FlairTagger(model=model, tokenizer=tokenizer, verbose=False)

# Store the predicted labels
predicted_labels = []

# Deidentify the texts and get the labels
for text in texts:
    documents = [Document(name='doc', text=text)]
    annotated_docs = tagger.annotate(documents)
    first_doc = annotated_docs[0]
    
    # Map the predicted labels to the ones in your dataset
    mapped_annotations = [
        Annotation(
            text=annotation.text,
            start=annotation.start,
            end=annotation.end,
            tag=tag_mapping.get(annotation.tag, annotation.tag), # use the original tag if no mapping found
            doc_id=annotation.doc_id,
            ann_id=annotation.ann_id
        )
        for annotation in first_doc.annotations
    ]
    
    predicted_labels.append({(annotation.start, annotation.end): annotation.tag for annotation in mapped_annotations})

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

# Write the DataFrame to a CSV file
report_df.to_csv('/media/pdef/E_ResearchData/2_ResearchData/Ruilin/deidentify_result.csv')
