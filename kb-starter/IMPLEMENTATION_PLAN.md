# 一页实施方案：文档型知识库（MVP）

## 目标
快速搭建一个文档型知识库：把 Markdown / 文档导入、切片、编码为向量，存入向量数据库，并支持简单的检索 + RAG 查询。

## 架构（简图）

```mermaid
flowchart LR
  A[Source Docs\n(Markdown / PDF / HTML)] --> B(Preprocessing \nsplit & clean)
  B --> C(Embeddings)
  C --> D[Vector DB \n(Chroma / Pinecone)]
  D --> E(Retrieval Layer \n(LlamaIndex / LangChain))
  E --> F[App / UI \n(Streamlit / Gradio / API)]
```

## 技术选型（推荐 MVP）
- 文档格式：Markdown 优先（易维护）
- 预处理与抽取：Python（分段/正则/markdown parsing）
- Embedding：OpenAI Embeddings（快速、效果好）或本地 sentence-transformers（合规）
- 向量数据库：Chroma（本地轻量）或 Pinecone（托管）
- 检索/应用层：LlamaIndex 或 LangChain + 简单 UI（Streamlit / Gradio）

## 步骤与估时（MVP）
- Step 0：准备示例文档（1 - 2 小时）
- Step 1：实现 Ingestion（分片 + embedding + 存储）—— 4 - 8 小时
- Step 2：实现简单检索 API & demo（Streamlit）—— 4 - 8 小时
- Step 3：测试与优化（chunk size、embedding 模型）—— 4 小时
总计（MVP）：约 1 - 3 个工作日（1 人）

## 估算成本（示例、粗略）
- 开发人员时间：按本地/远程资源不同而异
- OpenAI Embedding 成本：小规模试验（几千段）通常 < $20–100 / 月（取决于调用频率与模型）
- 向量 DB：Chroma 本地免费（磁盘与主机成本），Pinecone/Weaviate 有托管费用（按存储与请求计费）
- 部署：简单 demo 在一台小型云 VM（$5–20 / 月）即可

## 风险与合规点
- 敏感数据：若包含敏感信息，应优先考虑本地 embedding + 本地向量库，避免把原文或 embeddings 发送到第三方。
- 版权：抓取/包含的外部内容需确保合规与许可。

## 后续扩展（Roadmap）
- 增加增量更新（watch 文件夹 + 自动 ingest）
- 权限与搜索分组（multi-tenant）
- 更复杂的 QA（多轮对话 + citation）
- 部署到托管服务（Pinecone + VPC 模式 + 私有 LLM）

---

如需我把这份方案转成 PDF 或直接写入仓库 README 的“实施计划”部分，我可以马上替你完成。