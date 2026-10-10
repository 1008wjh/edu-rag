# Edu RAG

教育问答系统：FastAPI 提供 REST/WebSocket 接口，先用 BM25 + MySQL/Redis 命中结构化问答；未命中时可切换到 Milvus 混合检索和远程 LLM 生成答案。

## 架构

`static/index.html` → `app.py` → `IntegratedQASystem` → `BM25Search` → `Redis/MySQL`；当 `RAG_ENABLED=true` 时继续进入 `VectorStore`（Milvus、BGE-M3、reranker）和 DashScope。会话历史写入 MySQL，`/health` 可作为存活探针。

默认 `RAG_ENABLED=false`，避免 Web 进程启动时加载约 4GB 本地权重。模型文件、日志和密钥均不进入 Git；生产环境通过环境变量注入，模型应放在对象存储或独立的检索服务中。

## 启动

```bash
pip install -r requirements.txt
copy .env.example .env  # 按环境修改
uvicorn app:app --host 0.0.0.0 --port 9000
```

## 资源规划

| 阶段 | 配置 | 说明 |
| --- | --- | --- |
| Demo/面试演示 | 2 vCPU / 4 GB / 40 GB SSD | RAG 关闭，MySQL/Redis 可用托管服务 |
| 小规模内测 | API 2 vCPU/4 GB；MySQL 2 vCPU/4 GB；Redis 1 vCPU/1 GB；Milvus 4 vCPU/8 GB | API 与向量库分离，RAG 按需启用 |
| 生产起步 | API 2 副本×4 vCPU/8 GB；MySQL 4 vCPU/16 GB；Redis 2 GB；Milvus 8 vCPU/32 GB + SSD | 配置限流、连接池、监控和备份 |

## 后续加分方向

补充离线评测集（Recall@K、MRR、Faithfulness、P95 延迟）、可观测性（trace id/指标）、异步文档入库、权限与租户隔离、Docker Compose/Kubernetes 部署，以及 BM25→向量→rerank 的消融实验。
