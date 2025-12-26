from utils.vectors import storage_manager
from agents.base import init_embedding_model
from utils.loader import load_and_split_files

# initialize vector store for tool documentation
embedding_model = init_embedding_model().get_model()

shell_documentation_vector_store = storage_manager(
        collection_name="tools_documentation",
        persist_directory="store/vector_db",
        embedding_function=embedding_model
    )

files_path = "agents/tools_doc/"
docs = load_and_split_files(files_path, glob="md")

shell_documentation_vector_store.embed_documents(docs)
print("[bold green]Tool documentation updated successfully.[/bold green]")