import spacy
from typing import List
from tqdm import tqdm
import os

class Anonymizer:
    """Class containing methods to anonymize text via Named Entity Recognition using spaCy.

    Reference:
    https://spacy.io/usage/processing-pipelines
    """

    @classmethod
    def anonymize(cls, nlp: spacy.language.Language, documents: List, output_folder: os.PathLike) -> None:
        """Anonymize named entities in a list of documents.

        Args:
            nlp (spacy.language.Language): spaCy NLP pipeline.
            documents (List): List of documents to anonymize.
            output_folder (os.PathLike): Path to the output folder to save the anonymized Markdown files.
        """
        # Save the names of the documents
        doc_names = [doc.name for doc in documents]
        # Convert the extracted documents to Markdown format
        md_docs = [doc.export_to_markdown() for doc in documents]
        for i, doc in tqdm(enumerate(nlp.pipe(md_docs, disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])), desc=f"Anonymizing documents", total=len(md_docs)):
            # Anonymize named entities referring to people and organizations in the documents by replacing them with their entity type
            anonymized_doc = "".join([f"[{t.ent_type_}]"+t.whitespace_ if t.ent_type_ in ["ORG", "PERSON"] else t.text_with_ws for t in doc])
            # Save the anonymized documents to the output folder
            output_file = output_folder / f"{doc_names[i]}.md"
            with open(output_file, "w") as f:
                f.write(anonymized_doc)
        
        