# PDF Parser & Anonymizer
The code implements tools and utilities to parse PDF files using IBM's `docling` library and anonymize them using the Named Entity Recognition functionalities from `spacy`.

## Prerequisites
The entire pipeline runs locally, taking advantage of GPUs when available (both CUDA and MPS are supported) to speed up batch processing.

### Installation
1. Clone the repository:

   ```bash
   git clone 
   ```

2. Navigate to the project directory:

    ```bash
    cd 
    ```

3. Install the required dependencies (it is highly recommended to create a virtual environment):
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_trf
    ```

### Running the pipeline
For the script to run, you must specify a path to the folder containing the PDFs (it can also be the path to a single file).
Use the following command to run the project:

   ```bash
   python main.py <input_folder> <output_folder> 
   ```

You can run `python main.py --help` to see the script arguments (for instance, you can specify the path of the output folder to store the processed `.md` files).

> [!NOTE]  
> On the first run, `docling` will download the model weights locally from Hugging Face. For this reason, it might take a few minutes.
