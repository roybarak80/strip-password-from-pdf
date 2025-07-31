# PDF Password Stripper and JPG Converter

A Python tool to remove password protection from PDF files or convert them to JPG images.

## Features

- ✅ Remove password protection from PDF files
- ✅ Convert PDF pages to JPG/PNG images
- ✅ Process single files or entire directories
- ✅ Handle password-protected PDFs securely

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **For macOS users (if you get pdf2image errors):**
   ```bash
   brew install poppler
   ```

## Usage

### Remove Password Protection

**Single PDF file:**
```bash
python pdf_processor.py strip your_file.pdf --password YOUR_PASSWORD
```

**All PDFs in a directory:**
```bash
python pdf_processor.py strip /path/to/folder --password YOUR_PASSWORD
```

### Convert to JPG Images

**Single PDF file:**
```bash
python pdf_processor.py convert your_file.pdf --password YOUR_PASSWORD
```

**All PDFs in a directory:**
```bash
python pdf_processor.py convert /path/to/folder --password YOUR_PASSWORD
```

## Examples

**Remove password from salary.pdf:**
```bash
python pdf_processor.py strip salary.pdf --password mypassword123
```

**Convert salary.pdf to JPG images:**
```bash
python pdf_processor.py convert salary.pdf --password mypassword123
```

**Process all PDFs in current directory:**
```bash
python pdf_processor.py strip . --password mypassword123
```

**Convert all PDFs in Downloads folder:**
```bash
python pdf_processor.py convert ~/Downloads --password mypassword123
```

## Output Files

### Strip Mode
- Creates: `filename_unprotected.pdf`
- Original file remains unchanged
- New file has no password protection

### Convert Mode
- Creates folder: `filename_images/`
- Each page saved as: `filename_page_001.jpg`, `filename_page_002.jpg`, etc.
- Supports JPG and PNG formats

## Command Line Options

```bash
python pdf_processor.py {strip|convert} INPUT [OPTIONS]

Options:
  --password, -p    Password for the PDF(s) [REQUIRED]
  --output, -o      Output file or directory (optional)
  --format, -f      Image format: jpg or png (default: jpg)
  --dpi             DPI for image conversion (default: 200)
  --help            Show help message
```

## Troubleshooting

### "Command not found: pip"
Use `pip3` instead:
```bash
pip3 install -r requirements.txt
```

### "pdf2image" import errors
Install poppler on macOS:
```bash
brew install poppler
```

### "Incorrect password" error
- Double-check your password
- Make sure the PDF file is password-protected
- Try the password without extra spaces

### "File not found" error
- Make sure the PDF file exists in the specified path
- Use full path if needed: `/Users/username/Downloads/file.pdf`

## Tips

1. **Add your PDF files to the project directory** for easiest use
2. **Use the same password** for all PDFs from the same source
3. **Check the output** - files are saved in the same directory as input
4. **Backup important files** before processing

## Help

To see all available options:
```bash
python pdf_processor.py --help
``` 
