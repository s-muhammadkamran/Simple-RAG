from dotenv import load_dotenv
import json
import os
from pathlib import Path
from web_scraper import WebScraper

load_dotenv()

### IngestionHelper class is a utility class that provides methods for 
### reading environment variables and saving documents to files. 
### It includes methods to read environment variables with optional JSON 
### decoding and to save scraped documents to specified file locations.
class IngestionHelper:
    @classmethod
    def read_env_variable(cls, var_name, default=None, json_decode=False):
        value = os.getenv(var_name)
        if value is None and default is not None:
            return default
        elif value is None:
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

    ### The main method orchestrates the entire process of reading environment variables, 
    ### scraping documents from URLs, and saving them to files. It first reads the URLs and
    ### document names from environment variables, then uses the WebScraper class to scrape the
    ### documents, and finally saves the scraped documents to the specified file location.
    @classmethod
    def main(cls):
        # Step 1: Read the URLs and document names from environment variables
        url_doc_names = cls.read_env_variable("URL_DOC_NAMES", json_decode=True)
        url_list = cls.read_env_variable("URL_LIST", json_decode=True)
        files_loc = os.path.join(os.getcwd(), cls.read_env_variable("FILE_PATH", "docs"))    
        
        # Step 2: Scrape the documents from the provided URLs
        scraper = WebScraper(url_list)
        documents = scraper.scrape()
        print(f"Scraped {len(documents)} documents. Saving to {files_loc} folder...")

        # Step 3: Save the scraped documents to files
        cls.save_documents_to_files(documents, url_doc_names, files_loc)



### The script is designed to be run as a standalone program. 
### When executed, it will invoke the main method of the IngestionHelper class, 
### which orchestrates the entire process of reading environment variables, 
### scraping documents from URLs, and saving them to files.
if __name__ == "__main__":
    IngestionHelper.main()
