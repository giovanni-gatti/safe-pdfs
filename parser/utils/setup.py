import torch
import spacy
import logging
from docling.datamodel.pipeline_options import AcceleratorDevice, AcceleratorOptions, PdfPipelineOptions
from docling.datamodel.pipeline_options import TableStructureOptions
import multiprocessing


def init_logger() -> logging.Logger:
    """Initializes the logger."""
    logging.basicConfig(
        level=logging.INFO,  
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    _log = logging.getLogger(__name__)
    return _log


def config_spacy() -> spacy.language.Language:
    """Configures the spacy pipeline with the transformer model.
    
    Reference:
    https://spacy.io/usage/processing-pipelines
    """
    spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_trf")
    nlp.add_pipe("merge_entities")
    return nlp


def set_device() -> AcceleratorDevice:
    """Sets the device to use for the pipeline."""
    if torch.cuda.is_available():
        return AcceleratorDevice.CUDA
    elif torch.backends.mps.is_available():
        # MacOS Metal
        return AcceleratorDevice.MPS
    else:
        return AcceleratorDevice.AUTO
    

def config_accelerator() -> AcceleratorOptions:
    """Configures the accelerator options for the pipeline."""
    accelerator_options = AcceleratorOptions(
        device=AcceleratorDevice.MPS, 
        num_threads=multiprocessing.cpu_count()
    )
    return accelerator_options


def config_pipeline() -> PdfPipelineOptions:
    """Configures the pipeline options for the PDF extraction pipeline.
    
    Reference:
    https://ds4sd.github.io/docling/reference/pipeline_options/
    """
    pipeline_options = PdfPipelineOptions(
        accelerator_options=config_accelerator(),
        table_structure_options=TableStructureOptions(do_cell_matching=True),
        do_ocr=False,
        do_table_structure=True
    )
    return pipeline_options
