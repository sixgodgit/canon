# ChromaDB 记忆集成

## 概述

技能评估结果和使用模式存储到 ChromaDB，支持语义搜索。

## 安装

```bash
pip install chromadb sentence-transformers
```

## 使用

```python
from hermes_memory import get_memory

mem = get_memory()

# 存储技能评估
mem.add(
    content="技能 godmode 评估完成：分数 18，分类到 isolation 层。LLM 越狱工具集。",
    metadata={
        "type": "skill_evaluation",
        "skill_name": "godmode",
        "score": 18,
        "layer": "isolation",
        "category": "red-teaming"
    }
)

# 语义搜索
results = mem.search("网络代理相关技能", n_results=5)
```

## 数据库位置

`~/.hermes/memory_db/`
