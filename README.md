# RAG-QA-System

一个基于检索增强生成（RAG）的离线问答系统，支持文档上传、知识库构建和智能问答功能。

## 项目简介

本项目是一个完整的 RAG（Retrieval-Augmented Generation）问答系统，能够从上传的文档中提取知识，构建向量数据库，并基于文档内容进行智能问答。系统支持完全离线运行，无需依赖外部 API 服务。

## 环境要求

- Python 3.10+
- 所需依赖库：streamlit, langchain, langchain-text-splitters, chromadb, pypdf2, python-docx, python-dotenv

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/moon1285/RAG-QA-System-linyiming2405030253.git
cd RAG-QA-System-linyiming2405030253
```

### 2. 创建虚拟环境（可选但推荐）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. Ollama 安装（可选，用于在线推理）

如果需要使用真实的大语言模型进行推理，可以安装 Ollama：

#### Windows / macOS
```bash
# 下载并安装 Ollama
# 官网：https://ollama.com/

# 拉取模型
ollama pull deepseek-r1:7b
```

#### Linux
```bash
curl https://ollama.ai/install.sh | sh
ollama pull deepseek-r1:7b
```

## 使用说明

### 运行 Web 应用

```bash
streamlit run app.py
```

应用启动后，访问 `http://localhost:8501` 即可使用。

### 上传文档

1. 在左侧面板点击"选择文件"按钮
2. 选择 PDF、DOCX 或 TXT 格式的文档
3. 系统会自动处理文档并添加到知识库

### 加载默认文档

点击"加载默认文档"按钮，系统会自动加载 `docs/` 目录下的示例文档。

### 提问

1. 在右侧问答区域输入您的问题
2. 点击"提问"按钮
3. 系统会从知识库中检索相关内容并生成回答

### 清空知识库

点击"清空知识库"按钮可以清除所有已上传的文档和向量数据。

## 关键技术点

### RAG 流程

1. **文档加载**：支持 PDF、DOCX、TXT 等多种格式文档
2. **文本分块**：使用 `RecursiveCharacterTextSplitter` 将长文本切分为合适大小的片段
3. **向量化**：使用 `all-MiniLM-L6-v2` 模型将文本转换为向量
4. **向量存储**：使用 Chroma 向量数据库存储和检索向量
5. **问答生成**：基于检索到的上下文生成精准回答

### 所用模型

- **嵌入模型**：`all-MiniLM-L6-v2`（由 Chroma 默认提供）
- **语言模型**：支持离线 FakeLLM（默认）或通过 Ollama 使用真实模型

### 嵌入方式

系统使用 Chroma 的 `DefaultEmbeddingFunction`，基于 Sentence Transformers 的 `all-MiniLM-L6-v2` 模型进行文本嵌入，该模型轻量高效，适合离线部署。

### 离线运行

本项目支持完全离线运行：
- 使用本地嵌入模型进行向量转换
- 使用 FakeLLM 进行离线推理
- 无需启动外部服务或 Trae 客户端

## 项目结构

```
├── app.py              # Streamlit Web 应用
├── rag_qa.py           # RAG 问答链核心逻辑
├── knowledge_base.py   # 知识库管理模块
├── test_true_api.py    # API 测试脚本
├── .env                # 环境配置文件
├── requirements.txt    # 依赖列表
├── docs/               # 默认文档目录
└── chroma_db/          # 向量数据库存储目录
```

## 注意事项

1. 首次运行时，系统会自动下载嵌入模型（约 80MB）
2. 建议使用 Python 3.10+ 版本以确保兼容性
3. 如果需要使用真实 LLM，请配置 `.env` 文件并启动 Ollama 服务

## License

MIT License