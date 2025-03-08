import argparse
from pathlib import Path
from parser.utils.setup import config_spacy, init_logger
from parser.model.extract import Extractor
from parser.model.anonymize import Anonymizer


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process input and output paths for the input PDFs and output Markdown files.")
    # Required input path argument
    parser.add_argument('input_path', type=str, help="Path to the input file or folder.")
    # Optional output path argument
    parser.add_argument('output_path', type=str, nargs='?', default=None, help="Path to the output folder [optional].")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path) if args.output_path else None
    logger = init_logger()

    if not input_path.exists():
        raise ValueError("Input path must be a valid path to a file or folder.")

    if not output_path:
        output_path = input_path if input_path.is_dir() else input_path.parent
    elif not output_path.is_dir():
        raise ValueError("Output path must be a path to a valid folder.")
    
    nlp = config_spacy()
    if input_path.is_file():
        # Extract and anonymize a single document
        logger.info(f"Parsing the PDf file: {input_path}")
        doc = Extractor.extract(input_path)
        logger.info(f"Anonymizing the extracted text from: {input_path}")
        Anonymizer.anonymize(nlp, doc, output_path)
    elif input_path.is_dir():
        # Extract and anonymize multiple documents
        logger.info(f"Parsing the PDF files in the folder: {input_path}")
        docs = Extractor.batch_extract(input_path)
        logger.info(f"Anonymizing the extracted text from the PDF files in the folder: {input_path}")
        Anonymizer.anonymize(nlp, docs, output_path)
    logger.info(f"Parsed and anonymized documents saved to: {output_path}")


if __name__ == "__main__":
    main()