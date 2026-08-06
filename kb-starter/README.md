# KB Starter — 快速入门

这是一个最小可行的文档型知识库起始模板，包含示例文档、示例 ingestion 脚本与运行说明。目标：在本地几分钟内完成文档切片、embedding 并存入本地 Chroma 向量数据库，便于后续构建检索与 RAG 层。

目录结构（已包含在仓库中）：

- kb-starter/
  - README.md        ← 本文件（快速启动）
  - IMPLEMENTATION_PLAN.md ← 一页实施方案（架构图 + 技术选型 + 估时/估成本）
  - requirements.txt ← 运行依赖
  - ingest.py        ← 简单的 ingestion 脚本（读取 docs/*.md，做分片、生成 embedding、写入 Chroma）
  - docs/
    - sample.md      ← 示例文档

快速开始（3 步）：

1. 安装依赖

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r kb-starter/requirements.txt
   ```

2. 设置环境变量（需要 OpenAI key）

   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   # 可选：自定义 EMBEDDING_MODEL（默认使用 "text-embedding-3-small"）
   export EMBEDDING_MODEL="text-embedding-3-small"
   ```

3. 运行 ingestion（把 kb-starter/docs 下的 .md 导入到本地 Chroma）

   ```bash
   python kb-starter/ingest.py --docs_dir kb-starter/docs
   ```

脚本会在当前目录生成一个 ./chroma_db（持久化存储），并输出创建的 collection 名称与样本查询说明。

---

如果你希望我把代码直接合并到仓库的其它位置、或把 ingestion 改为使用 Pinecone/Weaviate、或改用纯开源的 embedding（如 sentence-transformers），告诉我我来调整。