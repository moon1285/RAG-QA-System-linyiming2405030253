import os
import json
from PyPDF2 import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

class KnowledgeBase:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.client = None
        self.collection = None
        
    def load_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    def load_docx(self, file_path):
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def load_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_document(self, file_path):
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == ".pdf":
            return self.load_pdf(file_path)
        elif ext == ".docx":
            return self.load_docx(file_path)
        elif ext == ".txt":
            return self.load_txt(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
    
    def batch_load_documents(self, folder_path):
        documents = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    text = self.load_document(file_path)
                    if text.strip():
                        documents.append({"filename": filename, "content": text})
                        print(f"已加载文件: {filename}")
                except Exception as e:
                    print(f"加载文件 {filename} 失败: {e}")
        return documents
    
    def split_text(self, documents, chunk_size=1000, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        all_chunks = []
        for doc in documents:
            chunks = text_splitter.split_text(doc["content"])
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "filename": doc["filename"],
                    "chunk_index": i,
                    "content": chunk
                })
        return all_chunks
    
    def init_chroma(self):
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="nlp_knowledge")
    
    def build_vector_store(self, chunks):
        if self.client is None:
            self.init_chroma()
        
        texts = [chunk["content"] for chunk in chunks]
        metadatas = [{"filename": chunk["filename"], "chunk_index": chunk["chunk_index"]} for chunk in chunks]
        ids = [f"doc_{i}" for i in range(len(chunks))]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print(f"向量库已构建完成，共 {len(chunks)} 个文本块")
    
    def add_documents(self, folder_path):
        documents = self.batch_load_documents(folder_path)
        chunks = self.split_text(documents)
        if self.client is None:
            self.init_chroma()
        
        if self.collection.count() == 0:
            self.build_vector_store(chunks)
        else:
            texts = [chunk["content"] for chunk in chunks]
            metadatas = [{"filename": chunk["filename"], "chunk_index": chunk["chunk_index"]} for chunk in chunks]
            ids = [f"doc_{self.collection.count() + i}" for i in range(len(chunks))]
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"已添加 {len(chunks)} 个文本块到向量库")
    
    def load_vector_store(self):
        if os.path.exists(self.persist_directory):
            self.init_chroma()
            print("向量库已加载")
        else:
            print("向量库不存在，请先构建")
    
    def search(self, query, k=3):
        if self.client is None:
            self.load_vector_store()
        
        if self.collection is None:
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'page_content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i]
            })
        return formatted_results
    
    def get_document_count(self):
        if self.client is None:
            self.load_vector_store()
        
        if self.collection is not None:
            return self.collection.count()
        return 0
    
    def clear_collection(self):
        if self.client is None:
            self.load_vector_store()
        
        if self.collection is not None:
            count = self.collection.count()
            if count > 0:
                self.collection.delete(ids=self.collection.get()['ids'])
                print(f"已清空 {count} 条数据")
            else:
                print("集合已为空")
            return True
        return False

if __name__ == "__main__":
    kb = KnowledgeBase()
    
    kb.add_documents("./docs")
    
    query = "什么是Transformer？"
    results = kb.search(query)
    print(f"\n查询: {query}")
    print("相关结果:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['metadata']['filename']}: {result['page_content'][:100]}...")