# 技能生态园丁决策树

## 核心决策流程

```
                      ┌─────────────┐
                      │  技能输入    │
                      │ (name,score │
                      │  anti,cat)  │
                      └──────┬──────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │  Step 1: 危险技能检查    │
              │  name in DANGEROUS_LIST? │
              └──────┬─────────────┬─────┘
                     │ 是          │ 否
                     ▼             ▼
              ┌──────────┐  ┌──────────────────┐
              │delete_can-│  │ Step 2: 重复检查 │
              │ didate    │  │ name in DUPLICATE│
              └──────────┘  │ LIST?            │
                            └──────┬──────┬────┘
                                   │ 是   │ 否
                                   ▼      ▼
                            ┌──────────┐  ┌───────────────────┐
                            │delete_can│  │ Step 3: 评分分类  │
                            │ didate   │  │ score < 25?       │
                            └──────────┘  └──────┬──────┬─────┘
                                                 │ 是   │ 否
                                                 ▼      ▼
                                          ┌────────┐  ┌────────────────┐
                                          │cold_st-│  │ score < 50?    │
                                          │ orage  │  └──────┬────┬────┘
                                          └────────┘    │ 是 │ 否
                                                         ▼    ▼
                                                  ┌────────┐ ┌────┐
                                                  │probat- │ │keep│
                                                  │ion     │ └────┘
                                                  └────────┘
```

## Anti-Entropy 覆盖规则

```
anti_entropy_flag = true 的技能：

    delete_candidate ──覆盖为──→ cold_storage
    cold_storage     ──保持──→ cold_storage
    probation        ──保持──→ probation
    keep             ──保持──→ keep
```

**核心：anti_entropy_flag=true 的技能永远不能被标记为 delete_candidate。**

## 一致性检查清单

执行前后必须逐一验证：

- [ ] 输出技能总数 == 输入技能总数
- [ ] 所有 anti_entropy_flag=true 的技能，recommended_action ≠ "delete_candidate"
- [ ] 所有 recommended_action="delete_candidate" 的技能，defense_notes 不少于 20 字
- [ ] 所有 recommended_action="cold_storage" 的技能，defense_notes 不少于 20 字
- [ ] JSON 格式可被 `python3 -c "import json; json.load(sys.stdin)"` 正确解析
- [ ] 不包含 report_metadata 或 summary 等附加元数据

## 争议技能处理指南

| 争议 | 倾向 | 理由 |
|:----|:----|:----|
| godmode 是红队工具，要不要保留？ | delete_candidate | 在无独立的红队测试环境时，留在生产系统中风险过高 |
| obliteratus 文档很详尽 | delete_candidate | 文档质量高≠技能安全。依赖 GPU 且无法执行，是死代码 |
| multi-model-analysis 我刚刚创建的 | cold_storage | 内容完整度不如 multi-model-collaboration，功能重复 |
| 有些 GPU 技能将来可能用上 | probation | 缓刑而非删除，保留未来可能性 |
| 下载/安装/启动服务器 | keep | 如果技能本身没问题，不能因为"一次性"就降级 |
