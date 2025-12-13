from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_aws import BedrockEmbeddings
from utils import AWSLLM
import hashlib
import os

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
RETRIEVER_K = 3

class KBRag:
    def __init__(
        self,
        pdf_path: str,
        persist_dir: str = "chroma_db",
        region: str = "us-east-1"
    ):
        self.pdf_path = pdf_path
        self.persist_dir = persist_dir
        self.hash_file = os.path.join(persist_dir, "doc.hash")

        # Embeddings
        self.embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1",
            region_name=region
        )

        # LLM 
        self.llm = AWSLLM()

        # Init / Reload Vector DB
        self.vectordb = self.load_or_create_vdb()

        # Retriever
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": RETRIEVER_K})

    def file_hash(self) -> str:
        with open(self.pdf_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def load_or_create_vdb(self):
        current_hash = self.file_hash()

        if os.path.exists(self.hash_file):
            with open(self.hash_file, "r") as f:
                saved_hash = f.read().strip()
        else:
            saved_hash = None

        if saved_hash == current_hash and os.path.exists(self.persist_dir):
            # Reuse existing DB
            return Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )

        if os.path.exists(self.persist_dir):
            import shutil
            shutil.rmtree(self.persist_dir)

        os.makedirs(self.persist_dir, exist_ok=True)

        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(documents)

        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

        with open(self.hash_file, "w") as f:
            f.write(current_hash)

        return vectordb
    
    # RAG Call
    def __call__(self, user_input: str) -> str:
        docs = self.retriever.invoke(user_input)
        context = "\n\n".join(d.page_content for d in docs)

        prompt = f"""
                    You are an HR support assistant.
                    Answer ONLY using the context below.
                    If the answer is not present, say:
                    "Information not available in the knowledge base."

                    Context:
                    {context}

                    Question:
                    {user_input}

                    Answer:
                    """

        return self.llm.chat(prompt)
