from dotenv import load_dotenv
import json
import os

load_dotenv()

from langchain_community.document_loaders import WebBaseLoader
from pathlib import Path

class WebScraper:
    def __init__(self, urls):
        self.urls = urls

    def scrape(self):
        all_documents = []
        for url in self.urls:
            loader = WebBaseLoader(url)
            documents = loader.load()
            all_documents.extend(documents)
        return all_documents

    @classmethod
    def read_env_variable(cls, var_name, default=None, json_decode=False):
        value = os.getenv(var_name)
        if value is None:
            if default is not None:
                return default
            else:
                raise ValueError(f"Environment variable '{var_name}' is not set and no default value was provided.")
        
        if json_decode:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON for environment variable '{var_name}': {e}")
        return value

    @classmethod
    def save_documents_to_files(cls, documents, doc_names, files_loc):
        if len(documents) != len(doc_names):
            print("Warning: The number of documents scraped does not match the number of document names provided.")
            print(f"Number of documents scraped: {len(documents)}")
            print(f"Number of document names provided: {len(doc_names)}")
            return

        try:
            # Check if the directory exists, if not, create it
            if not os.path.exists(files_loc):      
                os.makedirs(files_loc, exist_ok=True)
                print(f"Directory {files_loc} created successfully.")
            else:
                print(f"Directory {files_loc} already exists.")
        except OSError as e:
            print(f"Error creating directory {files_loc}: {e}")
            return

        for i, doc in enumerate(documents):
            print(f"Document {i+1}: {doc_names[i]}...") 
            # Write the document content to a text file @ docs folder    
            try:
                with open(os.path.join(files_loc, f"{doc_names[i]}.txt"), "w", encoding="utf-8") as f:
                    f.write(doc.page_content)                    
            except OSError as e:
                print(f"Error writing document {doc_names[i]}.txt: {e}")

def main():
    # Step 1: Read the URLs and document names from environment variables
    url_doc_names = WebScraper.read_env_variable("URL_DOC_NAMES", json_decode=True)
    url_list = WebScraper.read_env_variable("URL_LIST", json_decode=True)
    files_loc = os.path.join(os.getcwd(), WebScraper.read_env_variable("FILE_PATH", "docs"))    
    
    # Step 2: Scrape the documents from the provided URLs
    scraper = WebScraper(url_list)
    documents = scraper.scrape()
    print(f"Scraped {len(documents)} documents. Saving to {files_loc} folder...")

    # Step 3: Save the scraped documents to files
    WebScraper.save_documents_to_files(documents, url_doc_names, files_loc)

if __name__ == "__main__":
    main()