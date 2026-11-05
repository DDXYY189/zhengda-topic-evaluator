# Zhengda Topic Evaluator

正大杯全国大学生市场调查与分析大赛智能选题评审 Skill。

## 使用

将本仓库目录放入 Codex 工作区的 `.agents/skills/zhengda-topic-evaluator/`，或直接显式调用：

```text
$zhengda-topic-evaluator 评审这个候选题目：……
```

支持单题评估、多题比较、题目优化、创新性专项、调研可行性、案例检索和立项前终审。A“选题内在竞争力”和 B“团队执行可行性”始终独立展示。

## 内容

- `SKILL.md`：Skill 入口与模式路由。
- `references/`：评分、工作流、研究方法、规则、公共案例和隐私证据政策。
- `references/public_cases_2025_2026.csv`：2025—2026 年公开案例索引。
- `scripts/validate_scores.py`：校验双评分权重、锚点和未知项。
- `scripts/check_public_package.py`：阻断私有论文、完整 PDF、抽取文本和个人联系方式进入发行包。
- `assets/evaluation-template.md`：统一评审报告模板。

## 私有论文库

本仓库不包含任何完整参赛论文、问卷或用户私有资料。使用者可以在自己的工作区建立 `local_private_corpus/`，Skill 会优先使用本地 manifest/profile；没有私有库时自动退回公共案例库。

## 验证

```text
python scripts/validate_scores.py score.json
python scripts/check_public_package.py . --allow-public-case-index
```

发布前请确认 `国赛论文/`、`local_private_corpus/`、`extracted_text/`、完整 PDF 和联系方式都没有进入 Git 提交。
