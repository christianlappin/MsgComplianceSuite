# MsgComplianceSuite

## Overview
MsgComplianceSuite is a collection of Python tools designed for processing `.msg` files, particularly in compliance and auditing contexts. This suite includes tools for converting emails to PDFs and extracting email metadata, aiding in compliance audits, legal discovery, and data archiving.

## Tools

### Email to PDF Converter
Converts `.msg` files to PDF format, preserving email content, metadata, and embedded images.

- **Location**: `/EmailToPDFConverter`
- **Usage**:
  - Navigate to the `EmailToPDFConverter` directory.
  - Run `python email_to_pdf_converter.py`.
- **Requirements**: Detailed in `EmailToPDFConverter/requirements.txt`.

### Email Metadata Extractor
Extracts and compiles key metadata from `.msg` files into a structured format for analysis and reporting.

- **Location**: `/EmailMetadataExtractor`
- **Usage**:
  - Navigate to the `EmailMetadataExtractor` directory.
  - Run `python email_metadata_extractor.py`.
- **Requirements**: Detailed in `EmailMetadataExtractor/requirements.txt`.

## Installation
Clone this repository and navigate to the respective tool's directory. Install the required dependencies as listed in each tool's `requirements.txt`.

```bash
git clone https://github.com/christianlappin/MsgComplianceSuite.git
cd MsgComplianceSuite/[ToolDirectory]
pip install -r requirements.txt

