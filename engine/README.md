# Canon 自动化引擎

本目录包含 Canon v2.1 新增的热度检测与晋升/降级自动化引擎，用于辅助 Librarian 做出数据驱动的层级调整决策。

## 文件清单

### `heatmap.py` — 热度分析引擎

**功能**：读取 `~/.hermes/skills/.usage.json`，计算技能使用频率和趋势，输出热度图谱。

**运行方式**：
```bash
python3 heatmap.py [usage_file_path]
```

**输出**：
- 控制台报告：Top 20 热门技能、Bottom 10 冷门技能、趋势分布统计
- JSON 导出：`heatmap-report.json`（与 `.usage.json` 同目录）

**计算指标**：
- 总调用次数（`use_count`）
- 最后使用距今天数（`last_used_at`）
- 查看/修改次数（`view_count`、`patch_count`）
- 热度评分（0-100）
- 趋势标签：`hot` / `active` / `cooling` / `cold` / `stale`

**用途**：帮助识别"被低估"的高频技能（应考虑晋升）和"僵尸"低频技能（应考虑降级）。

---

### `promotion.py` — 晋升/降级规则引擎

**功能**：根据使用频率自动生成层级调整建议。

**运行方式**：
```bash
python3 promotion.py [usage_file_path] [classification_file_path]
```

**默认路径**：
- `usage_file`: `~/.hermes/skills/.usage.json`
- `classification_file`: `~/.hermes/skills/autonomous-ai-agents/canon/references/librarian-classification.json`

**规则**：
- **高频晋升**：近 30 天调用 > 50 次 → 建议升级至 🚀 热气层
- **低频降级**：近 90 天调用 < 3 次 → 建议降级入 🌱 种子库
- **多样性保护**：`anti_entropy_flag=true` 的技能不参与自动降级
- **隔离层豁免**：`librarian_layer=quarantine` 的技能不参与自动晋升/降级，需走人工审批流程（见 `references/isolation-policy.md`）
- **容量守卫**：热气层最多 15 个，晋升建议超额时按调用量排序，仅保留前 N 个高置信度建议

**输出**：
- 控制台报告：晋升/降级建议列表及理由
- JSON 导出：`promotion-recommendations.json`（与 `.usage.json` 同目录）

**重要**：本引擎**只产出建议**，不直接改写 `librarian-classification.json`。最终层级变更需人工确认或由 Canon 主流程二次校验后写入。

---

## 集成到 Canon 主流程

参见 `SKILL.md` 步骤 2.5"热度检测与自动轮转"：

1. 运行 `heatmap.py` 获取热度图谱
2. 运行 `promotion.py` 获取晋升/降级建议
3. 将建议并入本轮评估结果，用于步骤 3"热度感知轮转"

替代纯随机/凭直觉的轮转逻辑，用真实使用数据驱动生态调整决策。

---

## 数据说明

当前 `.usage.json` 只记录累计 `use_count` 和 `last_used_at` 等快照字段，没有逐次调用的时间序列日志。因此：

- 近 30/90 天调用数是**估算值**（见 `promotion.py` 中 `estimate_recent_calls()` 函数注释）
- 估算逻辑：如果 `last_used_at` 超出窗口，估算为 0；如果在窗口内，用 `use_count` 作为上限

**如果未来 `.usage.json` 升级为记录时间序列**（如 `usage_log.jsonl`），应替换估算逻辑为精确统计，移除 `estimate_recent_calls()` 中的保守估算警告。

---

## 依赖

- Python 3.7+
- 标准库：`json`, `datetime`, `pathlib`（无第三方依赖）

---

## 许可

与 Canon 主技能相同，采用 MIT 许可。
