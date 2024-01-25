import os
import extract_msg
import pdfkit
from bs4 import BeautifulSoup
import base64

def read_msg_file(msg_file):
    """
    Reads an MSG file and extracts its content and attachments.
    """
    with extract_msg.Message(msg_file) as msg:
        subject = msg.subject
        body = msg.body
        html_body = msg.htmlBody
        received = msg.date
        attachments = [
            {
                'cid': getattr(att, 'cid', None),
                'data': att.data,
                'longFilename': att.longFilename,
                'mime': getattr(att, 'mime', None)
            }
            for att in msg.attachments if hasattr(att, 'data') and att.longFilename
        ]

    return subject, body, html_body, received, attachments

def create_pdf(html_content, output_file):
    """
    Creates a PDF from HTML content.
    """
    options = {'encoding': "UTF-8", 'no-images': ''}
    pdfkit.from_string(html_content, output_file, options=options)

def convert_folder(directory):
    """
    Converts all MSG files in a specified directory to PDFs.
    """
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    msg_files = [f for f in os.listdir(directory) if f.endswith('.msg')]
    if not msg_files:
        print("No .msg files found in the specified directory.")
        return

    for filename in msg_files:
        try:
            msg_file = os.path.join(directory, filename)
            base_filename = os.path.splitext(filename)[0]
            subject, body, html_body, received, attachments = read_msg_file(msg_file)

            # Process HTML content
            embedded_html = process_html_content(html_body, subject, received, attachments)
            
            # Save the email as PDF
            pdf_output_file = os.path.join(directory, base_filename + '.pdf')
            create_pdf(embedded_html, pdf_output_file)
            print(f'Converted {msg_file} to {pdf_output_file}')

            # Extract PDF attachments
            extract_pdf_attachments(attachments, directory, base_filename)

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

def process_html_content(html_body, subject, received, attachments):
    """
    Processes the HTML content of the email, embedding images.
    """
    if html_body:
        soup = BeautifulSoup(html_body, 'html.parser')
        embed_images_in_soup(soup, attachments)
        soup.body.insert(0, BeautifulSoup(f"<h1>{subject}</h1><p>Received: {received}</p>", 'html.parser'))
        return str(soup)
    else:
        return f"<h1>{subject}</h1><p>Received: {received}</p><p>{body}</p>"

def embed_images_in_soup(soup, attachments):
    """
    Embeds images in the soup object.
    """
    for img in soup.find_all("img"):
        cid = img.get('src').lstrip('cid:')
        for att in attachments:
            if att['cid'] == cid and att['mime']:
                encoded_img = base64.b64encode(att['data']).decode()
                img['src'] = f"data:{att['mime']};base64,{encoded_img}"
                break

def extract_pdf_attachments(attachments, directory, base_filename):
    """
    Extracts PDF attachments from the email.
    """
    for att in attachments:
        if att['longFilename'].endswith('.pdf'):
            pdf_attachment_file = os.path.join(directory, f"{base_filename}_{att['longFilename']}")
            with open(pdf_attachment_file, 'wb') as pdf_file:
                pdf_file.write(att['data'])
            print(f"Extracted PDF attachment as {pdf_attachment_file}")

# Prompt the user for the directory path
directory_path = input("Enter the directory path containing .msg files: ")
convert_folder(directory_path)

