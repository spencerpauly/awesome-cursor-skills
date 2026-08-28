---
name: alibaba-java-coding-guidelines
description: Enforce the Alibaba Java Development Manual (Huangshan v1.7.1, 327 rules) as the coding standard for Java projects. Use when writing, modifying, reviewing, or refactoring Java code; when discussing or querying Java coding conventions (naming, constants, OOP, collections, concurrency, control flow, comments, exceptions, logging, unit tests, security, MySQL, engineering structure, design); or when a standards-aligned code review is needed. 编写、修改、评审 Java 代码，讨论 Java 编码规约，或需按《阿里巴巴 Java 开发手册（黄山版）》规约自查与评审时使用。
agent_created: true
---

# Alibaba Java Coding Guidelines（阿里巴巴 Java 开发手册规约）

将《Java 开发手册（黄山版）》（v1.7.1，327 条规约）作为 Java 日常开发的**强制约束规范**：编码前自查、评审时逐项核对、有疑问时查原文。

## 何时使用

- 编写、修改、重构任何 Java 代码（`server/`、`ops-be/`、`jobhunter-shared/` 等 Java 工程）之前与之中。
- 对 Java 代码做 code review / 评审 / 质量检查。
- 讨论或查询 Java 编码规范条目（命名、常量、OOP、集合、并发、控制语句、注释、异常、日志、单测、安全、MySQL、工程结构、设计规约）。

## 使用流程

### 1. 编码时自查（写/改代码前加载）

1. 加载 `references/review-checklist.md`，按当前改动涉及的章节逐项自查（命名风格 → OOP → 集合/并发 → 异常日志 → MySQL 等）。
2. 改动范围只涉及某章节时，可只查对应小节。
3. 拿不准的条目打开 `references/java-coding-guidelines.md` 查正例/反例原文（用 grep 定位章节，如 `grep -n "魔法值" references/java-coding-guidelines.md`）。
4. 自查发现的违规立即修复再提交，不把问题留到评审。

### 2. 评审时核对（review 时逐项勾选）

1. 加载 `references/review-checklist.md`，按受影响章节逐项核对。
2. 每个违规记录为 `文件:行号 - 违反条款 - 建议`，最后用清单末尾的「评审结论模板」输出：结论（通过/有条件通过/不通过）+ 强制违规数 + 推荐改进数 + 问题清单。
3. 【强制】违规必须阻断合并；【推荐】/【参考】作为改进建议提出。
4. 涉及 MySQL 的改动必须核对建表/SQL/索引/ORM 四节；涉及对外接口必须核对幂等与兼容性。

### 3. 查询规约原文

- 完整手册：`references/java-coding-guidelines.md`（七大章 + 附1 版本历史 + 附2 专有名词 + 附3 错误码列表，含全部正例/反例/说明与 78 个 Java 示例代码块）。
- 检索示例：`grep -n "线程池" references/java-coding-guidelines.md`；错误码直接查附3 表格。

### 4. 更新手册（仅当上游发布新版本时）

1. 确认官方最新版：`https://github.com/alibaba/p3c` 仓库根目录的 PDF。
2. 运行 `scripts/update_guidelines.py`（自动下载官方 PDF → 提取文本 → 重建 markdown），覆盖 `references/java-coding-guidelines.md`。
3. 依赖：`pip install pymupdf`；Python ≥ 3.9。
4. 重新生成后，用脚本输出末尾的统计（强制/推荐/参考条数）与上一版对比，确认无异常丢失；`review-checklist.md` 如需同步新增条目再手工更新。
5. 手册为自动转录产物，禁止手工编辑正文；如转录有瑕疵，修 `scripts/update_guidelines.py` 后重新生成。

## 资源结构

| 文件 | 作用 |
| --- | --- |
| `references/java-coding-guidelines.md` | 手册全文（327 条规约 + 正反例 + 附1/2/3），权威引用源 |
| `references/review-checklist.md` | 可勾选评审清单（按章节组织的高频强制点 + 评审结论模板） |
| `scripts/update_guidelines.py` | 官方 PDF → markdown 转录管线（下载/提取/重建一体） |

## 注意

- 手册/清单均源自阿里巴巴官方 p3c（Apache-2.0）；本文档与其同协议。
- 规约有【强制】【推荐】【参考】三档：评审阻断仅针对【强制】；【推荐】高价值改进；【参考】视场景采纳。
