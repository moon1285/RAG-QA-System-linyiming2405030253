import streamlit as st
import os
import tempfile
from knowledge_base import KnowledgeBase
from rag_qa import RAGQA

def main():
    st.set_page_config(page_title="NLP知识库问答系统", page_icon="📚", layout="wide")
    
    st.title("📚 NLP知识库问答系统")
    
    if "kb" not in st.session_state:
        st.session_state.kb = KnowledgeBase()
        st.session_state.kb.load_vector_store()
    
    if "rag" not in st.session_state:
        st.session_state.rag = RAGQA()
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    if "refresh_trigger" not in st.session_state:
        st.session_state.refresh_trigger = 0
    
    def trigger_refresh():
        st.session_state.refresh_trigger += 1
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📤 文档上传")
        
        uploaded_files = st.file_uploader(
            "选择PDF、DOCX或TXT文件",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            key=f"file_uploader_{st.session_state.refresh_trigger}"
        )
        
        if uploaded_files:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files):
                if file.name not in st.session_state.uploaded_files:
                    status_text.text(f"正在处理: {file.name}")
                    
                    with tempfile.TemporaryDirectory() as temp_dir:
                        file_path = os.path.join(temp_dir, file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getvalue())
                        
                        docs = st.session_state.kb.batch_load_documents(temp_dir)
                        chunks = st.session_state.kb.split_text(docs)
                        
                        if st.session_state.kb.client is None:
                            st.session_state.kb.init_chroma()
                        
                        if st.session_state.kb.collection.count() == 0:
                            st.session_state.kb.build_vector_store(chunks)
                        else:
                            texts = [chunk["content"] for chunk in chunks]
                            metadatas = [{"filename": chunk["filename"], "chunk_index": chunk["chunk_index"]} for chunk in chunks]
                            ids = [f"doc_{st.session_state.kb.collection.count() + i}" for i in range(len(chunks))]
                            st.session_state.kb.collection.add(
                                documents=texts,
                                metadatas=metadatas,
                                ids=ids
                            )
                    
                    st.session_state.uploaded_files.append(file.name)
                    progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.text("处理完成！")
            st.success(f"已成功上传 {len(uploaded_files)} 个文件")
        
        st.subheader("📊 知识库状态")
        doc_count = st.session_state.kb.get_document_count()
        st.metric(label="文本块数量", value=doc_count)
        
        if st.session_state.uploaded_files:
            st.write("已上传的文档:")
            for file in st.session_state.uploaded_files:
                st.write(f"- {file}")
        
        st.subheader("⚙️ 操作")
        
        if st.button("📥 加载默认文档"):
            with st.spinner("正在加载默认文档..."):
                st.session_state.kb.add_documents("./docs")
                default_docs = os.listdir("./docs")
                for doc in default_docs:
                    if doc not in st.session_state.uploaded_files:
                        st.session_state.uploaded_files.append(doc)
                st.success("默认文档已加载")
        
        if st.button("🗑️ 清空知识库"):
            with st.spinner("正在清空知识库..."):
                st.session_state.kb.clear_collection()
                st.session_state.chat_history = []
                st.session_state.uploaded_files = []
                trigger_refresh()
                st.success("知识库已清空")
    
    with col2:
        st.subheader("💬 问答交互")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        user_input = st.text_input("请输入您的问题:", key="user_input")
        
        if st.button("提问") and user_input.strip():
            with st.spinner("正在检索和生成答案..."):
                answer = st.session_state.rag.answer(user_input, st.session_state.chat_history)
                
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                
                st.rerun()
        
        if st.button("清空对话"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()