import os
from pdfminer.high_level import extract_text


# function to convert pdf to txt file
def pdf_to_txt(pdf_file_path, output_txt_path):
    # Extract text from the PDF file
    text = extract_text(pdf_file_path)

    # Save the extracted text to a .txt file
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# Path to the folder containing PDF files
pdf_folder = 'data'

# Iterate through all files in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_file_path = os.path.join(pdf_folder, filename)

        # creating the output.txt file by replacing the extension
        output_txt_path = os.path.splitext(pdf_file_path)[0] + '.txt'

        # Convert PDF to TXT and save
        pdf_to_txt(pdf_file_path, output_txt_path)

        print(f"Text saved to: {output_txt_path}")
