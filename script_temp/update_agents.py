import sys

path = "AGENTS.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add custom rule 6
old_rule = "5. 修改 .yml 时（Dify agent 配置），必须做 YAML 语法 + Dify DSL 结构校验"
new_rule = (
    "5. 修改 .yml 时（Dify agent 配置），必须做 YAML 语法 + Dify DSL 结构校验\n"
    " 6. **每次 Task 完成后提交并推送 GitHub**："
    "完成一个可独立验收的 Task 后，"
    "必须 git add -A && git commit -m \"feat: ...\" && git push。"
    "方便出问题时回滚到稳定版本。commit message 需简明描述做了什么。"
)
if old_rule in content:
    content = content.replace(old_rule, new_rule)
    print("1. custom rule 6 added")
else:
    print("1. SKIP: old_rule not found")

# 2. Add version management section
old_section = "| 当前阶段 | 基线尚未运行，索引尚未构建，API 尚未搭建 |\n \n ---"
new_section = (
    "| 当前阶段 | 基线尚未运行，索引尚未构建，API 尚未搭建 |\n"
    " \n"
    " ---\n"
    " \n"
    " ## 版本管理\n"
    " \n"
    " - 远端仓库：origin \u2192 https://github.com/shuizjsztx02/tcg-embedding-service.git\n"
    " - 初始 commit：cf68f57 \u2014 feat: 初始化 TCG 卡牌视觉匹配服务项目\n"
    " - **分支策略**：日常开发在 main 分支进行；每次 Task 完成后提交并推送，确保每个 Task 的完成状态在 Git 历史中可追溯。\n"
    " - **回滚**：如果某个 Task 引入问题，用 git log 找到上一个稳定 commit，git revert 或 git reset --hard 回退，然后 git push --force-with-lease（仅限单人开发场景）。\n"
    " - **提交规范**：\n"
    "   - eat: ... \u2014 新功能或新 Task 完成\n"
    "   - ix: ... \u2014 修复 bug\n"
    "   - docs: ... \u2014 文档更新\n"
    "   - efactor: ... \u2014 重构\n"
    "   - chore: ... \u2014 基础设施（gitignore、依赖等）\n"
    "   - commit message 用中文或英文均可，但需简明描述做了什么以及为什么。\n"
    " \n"
    " ---"
)
if old_section in content:
    content = content.replace(old_section, new_section)
    print("2. version management section added")
else:
    print("2. SKIP: old_section not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
