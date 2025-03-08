from typing import List
import os
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from parser.utils.setup import config_pipeline

class Extractor:
    """Class containing methods to extract text from PDF documents using IBM's Docling library.

    Reference:
    https://ds4sd.github.io/docling/
    """

    converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PDF # Only PDF files are allowed, raises error if other formats are passed
        ],
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=config_pipeline())
        }
    )

    @classmethod
    def extract(cls, path: os.PathLike) -> List:
        """Extract text from a single PDF document.

        Args:
            path (os.PathLike): Path to the PDF document.
        """
        result = cls.converter.convert(path)
        return [result.document]

    @classmethod
    def batch_extract(cls, folder_path: os.PathLike) -> List:
        """Extract text from multiple PDF documents.

        Args:
            folder (os.PathLike): List of paths to the PDF
        """
        input_doc_paths = [path for path in folder_path.iterdir()]
        if len(input_doc_paths) == 1:
            # If only one document is present, extract it using the extract method
            return cls.extract(input_doc_paths[0])
        else:
            # If multiple documents are present, perform batch extraction instead
            conv_results = cls.converter.convert_all(
                input_doc_paths,
                raises_on_error=True
            ) 
            return [result.document for result in conv_results]