import json
from deidentify.base import Document
from deidentify.taggers import FlairTagger
from deidentify.tokenizer import TokenizerFactory
from deidentify.base import Annotation

def pretty_format(text, true_label, predicted_label):
    return "Text: {}\nTrue Label: {}\nPredicted Label: {}\n{}\n".format(text, true_label, predicted_label, '='*30)

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

texts = []
true_labels = []

INPUT_JSONL = '/media/bigdata/2. Gebruik en toepassing van data/20_12_18_Pablo_Mosteiro_Anonymization/prodigy/texts_namen_met_ano_out/texts_namen_met_ano.jsonl'
with open(INPUT_JSONL, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        texts.append(data['text'])
        if 'spans' in data:
            true_labels.append({(span['start'], span['end']): span['label'] for span in data['spans']})
        else:
            true_labels.append({})

model = 'model_bilstmcrf_ons_fast-v0.2.0'
tokenizer = TokenizerFactory().tokenizer(corpus='ons', disable=("tagger", "ner"))
tagger = FlairTagger(model=model, tokenizer=tokenizer, verbose=False)

predicted_labels = []
for text in texts:
    documents = [Document(name='doc', text=text)]
    annotated_docs = tagger.annotate(documents)
    first_doc = annotated_docs[0]
    mapped_annotations = [
        Annotation(
            text=annotation.text,
            start=annotation.start,
            end=annotation.end,
            tag=tag_mapping.get(annotation.tag, annotation.tag),
            doc_id=annotation.doc_id,
            ann_id=annotation.ann_id
        )
        for annotation in first_doc.annotations
    ]
    predicted_labels.append({(annotation.start, annotation.end): (annotation.tag, annotation.text) for annotation in mapped_annotations})

OUTPUT_TXT = '/media/pdef/E_ResearchData/2_ResearchData/Ruilin/deidentify_errors.txt'
with open(OUTPUT_TXT, 'w', encoding='utf-8') as output_file:
    for text, true_label, predicted_label in zip(texts, true_labels, predicted_labels):
        output_file.write(pretty_format(text, true_label, predicted_label))
