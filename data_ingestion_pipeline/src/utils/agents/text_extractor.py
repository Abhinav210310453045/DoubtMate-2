import os
import asyncio
import aiofiles
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

class DataExtract:
    def __init__(self, pdf_path, tool_name, max_workers=4):
        self.pdf_path = pdf_path
        self.pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        self.text_folder = f"{self.pdf_name}_text_{tool_name}"
        self.max_workers = max_workers
        os.makedirs(self.text_folder, exist_ok=True)

    async def _extract_page_async(self, page_num, page_layout):
        """Asynchronously extract text from a single page and save it to a file."""
        print(f"Processing Page {page_num} (async)")
        page_folder = os.path.join(self.text_folder, f"page_{page_num}")
        os.makedirs(page_folder, exist_ok=True)
        text_file_path = os.path.join(page_folder, f"page_{page_num}.txt")
        async with aiofiles.open(text_file_path, "w", encoding="utf-8") as text_file:
            await text_file.write(f"Page {page_num}\n\n")
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    await text_file.write(element.get_text())
        print(f"Saved: {text_file_path}")

    async def extract_text_pdfminer_async(self):
        """Extract text using asyncio for efficiency."""
        loop = asyncio.get_event_loop()
        tasks = []
        for page_num, page_layout in enumerate(extract_pages(self.pdf_path), start=1):
            tasks.append(self._extract_page_async(page_num, page_layout))
        await asyncio.gather(*tasks)
        print(f"Total Pages Processed: {len(tasks)}")



