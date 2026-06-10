# 贡献指南

感谢你愿意改进 KK 策展助手。这个仓库沉淀的是一套展览前策工作流，因此贡献时请优先保持方法论清晰、边界克制、表达可复用。

## 可以贡献什么

- 修正文档错别字、安装说明、表格表达。
- 补充更清晰的策展流程说明，但不要加入真实甲方、企业或未脱敏项目名称。
- 改进 `scripts/generate_brief_form.py` 的表单字段、样式或兼容性。
- 补充新的项目类型参考时，请先说明它与现有 A/B/C 三类的差异。

## 提交前检查

请至少运行：

```bash
python3 -m py_compile scripts/generate_brief_form.py
python3 scripts/generate_brief_form.py a /tmp/kk-exhibition-planner-check
```

如果修改了 README，请确认：

- 中文 README 与英文 README 的核心信息一致。
- 没有出现真实甲方项目名、企业名或未授权引用。
- 没有把本 Skill 描述成能生成完整展览文本、设计图或真实 PPTX 文件。

## Pull Request 建议

- 一个 PR 只解决一个清晰问题。
- 在 PR 描述中写明改动范围、验证方式和可能影响。
- 文档更新请尽量附上修改前后的差异说明。

## 许可

提交到本仓库的内容默认以 MIT License 发布。
