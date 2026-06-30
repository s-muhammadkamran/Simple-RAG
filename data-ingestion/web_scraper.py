from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import WebBaseLoader

### This script is responsible for scraping documents from a list 
### of URLs and returns them as a list of documents.
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