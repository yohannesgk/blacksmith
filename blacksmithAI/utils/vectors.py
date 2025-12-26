from langchain_chroma import Chroma
from rich import print

class storage_manager:

    def __init__(self, collection_name = 'example' ,persist_directory: str = "vector_db", embedding_function=None):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding = embedding_function

        self.client = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding
            )

    def get_client(self):
        return self.client
    
    def embed_documents(self, documents):
        self.client.add_documents(documents=documents)
        print(f"[bold green]Documents embedded and stored in collection '{self.collection_name}' successfully.[/bold green]")

    def query(self, query_text, n_results: int = 5, filter: dict = None):
        results = self.client.similarity_search(query_text, k=n_results, filter=filter)
        return results