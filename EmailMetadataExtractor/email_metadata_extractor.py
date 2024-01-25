import os
import extract_msg
import csv

def extract_metadata_from_msg(msg_file):
    try:
        with extract_msg.Message(msg_file) as msg:
            return {
                'From': msg.sender,
                'To': msg.to,
                'Cc': msg.cc,
                'Bcc': msg.bcc,
                'Date': msg.date,
                'Subject': msg.subject,
                'AttachmentNames': ', '.join(att.longFilename for att in msg.attachments if hasattr(att, 'longFilename'))
            }
    except Exception as e:
        print(f"Error processing file {msg_file}: {e}")
        return None

def process_directory(directory):
    metadata_list = []

    for filename in os.listdir(directory):
        if filename.lower().endswith('.msg'):
            msg_path = os.path.join(directory, filename)
            metadata = extract_metadata_from_msg(msg_path)
            if metadata:
                metadata_list.append(metadata)
        else:
            print(f"Skipping non-msg file: {filename}")

    if metadata_list:
        # Save metadata to a CSV file
        output_file = os.path.join(directory, 'email_metadata.csv')
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=metadata_list[0].keys())
            writer.writeheader()
            writer.writerows(metadata_list)
        print(f"Metadata extracted and saved to {output_file}")
    else:
        print("No valid .msg files found for processing.")

# Prompt the user for the directory path
directory_path = input("Enter the directory path containing .msg files: ")
process_directory(directory_path)

