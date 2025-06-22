from src.utils.agents.Base_agent import BaseAgent
import aiofiles
import os

class TextCleanerAgent(BaseAgent):
    def __init__(self, name, output_folder="cleaned_text"):  
        super().__init__(name)
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        
    async def clean_text(self, text):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that cleans and structures text while maintaining its original meaning."},
            {"role": "user", "content": "Clean and structure the following text. Remove unnecessary repetition, correct broken sentences, and organize tabular data properly. Ensure that topics within the text are structured logically. IMPORTANT: Do Not Try to change the text or add any knowledge by yourself, just remove or correct  the wrong part."},
            {"role": "user", "content": text}
        ]
        response = await self.llm.ainvoke(messages)  # Using async invoke
        return response.content.strip()
    
    async def process_pdf_text(self, pdf_texts, output_file="structured_output.txt"):  
        cleaned_texts = []
        for page_num, text in enumerate(pdf_texts, start=1):
            print(f"Processing page {page_num}...")
            cleaned_texts.append(await self.clean_text(text))  # Awaiting async call
        
        output_path = os.path.join(self.output_folder, output_file)
        
        async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
            await f.write("\n\n".join(cleaned_texts))  # Asynchronous file writing
        
        print(f"Processed text saved to: {output_path}")
        return output_path



# Example usage:
# import asyncio
# pdf_texts = ["Page 1 text here", "Page 2 text here"]
# agent = TextCleanerAgent("Text_Cleaner")
# asyncio.run(agent.process_pdf_text(pdf_texts))
