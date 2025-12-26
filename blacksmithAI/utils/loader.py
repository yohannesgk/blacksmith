from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_files(path: str, glob: str = "md", loader_cls=TextLoader):

    loader = DirectoryLoader(
        path, 
        glob=f"**/*.{glob}", 
        loader_cls=loader_cls
   )
    
    documents = loader.load()
    
    return documents

def load_and_split_files(path: str, glob: str = "md", loader_cls=TextLoader, chunk_size: int = 1000, chunk_overlap: int = 200):

    loader = DirectoryLoader(
        path, 
        glob=f"**/*.{glob}", 
        loader_cls=loader_cls
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    docs = loader.load_and_split(text_splitter)

    return docs