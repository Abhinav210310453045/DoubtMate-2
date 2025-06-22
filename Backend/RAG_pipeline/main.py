from src.utils.agents.text_extractor import DataExtract

def main():
    pdf_path = "DataBase/jesc101.pdf"  # Replace with actual PDF path
    tool_name = "pdfminer"

    extractor = DataExtract(pdf_path, tool_name, max_workers=8)  # Adjust workers as needed
    extractor.extract_text_pdfminer()

if __name__ == "__main__":
    main()