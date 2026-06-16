# Vision Harness Skill

[English README](README.en.md)

Vision Harness Skill 是一个面向 Agent 的结构化视觉理解技能包。

它的目标不是重新训练一个多模态模型，而是为 Agent 提供一层“视觉理解 Harness”：

* 让文字类 LLM Agent 通过结构化视觉包间接理解图片。
* 让多模态 LLM Agent 按照证据、区域、不确定性和任务模板更稳定地分析图片。

当前版本重点支持三类场景：

1. 技术截图诊断
2. UI 截图分析与语义级 HTML 重构
3. 流程图 / 泳道图的初步结构化与 SOP 草稿生成

---

## 为什么需要这个项目

很多 Agent 在处理图片时会遇到两个问题。

第一，文字类 LLM 没有原生视觉能力，无法直接读取截图、流程图和 UI 原型。

第二，多模态 LLM 虽然能“看图”，但经常直接跳到结论，缺少可复核的证据链，也不稳定地区分事实、推测和不确定点。

Vision Harness Skill 试图解决的不是“让模型变聪明”，而是让 Agent 的视觉分析过程更结构化、更可复核、更适合后续任务执行。

---

## 核心能力

### 1. Text-only Agent Mode

用于文字类 LLM Agent。

图片会先被转换为结构化的 `visual_packet`，包括：

* 图片尺寸、方向、主色调、亮度和复杂度
* OCR 文本块
* 文本行分组
* 区域划分
* 关键证据引用
* 空间布局线索
* Agent 推荐阅读指令

文字类 LLM 可以基于这些信息完成截图诊断、UI 分析或流程图初步结构化。

### 2. Multimodal Agent Mode

用于多模态 LLM Agent。

多模态 Agent 可以直接看原图，同时使用 Skill 提供的协议和模板，强制输出：

* observed_facts：图中直接可见的事实
* inferences：基于事实做出的推测
* evidence_quotes：关键 OCR 证据
* evidence_regions：证据区域
* uncertainties：不确定点
* recommended_actions：下一步动作

---

## 适用场景

### 技术截图诊断

适合包含大量日志、错误信息、配置项、命令行输出或软件界面的截图。

示例任务：

```text
请根据这张截图诊断错误原因，并给出可执行的修复建议。
```

### UI 截图分析与 HTML 重构

适合分析产品原型、后台页面、仪表盘、管理界面等 UI 截图。

支持三种模式：

* `ui_audit`：UI 结构和问题分析
* `ui_semantic_rebuild`：语义级 HTML 重构
* `ui_fidelity_clone`：尽量保持布局的高保真复刻辅助

注意：HTML 复刻质量不仅取决于本 Skill，也取决于驱动 Agent 的模型本身的前端代码能力。

### 流程图 / 泳道图初步结构化

适合从流程图中提取：

* 阶段
* 角色 / 泳道
* 节点
* 候选边
* 初步 SOP 草稿
* 需要人工确认的缺口

当前版本对箭头方向和复杂拓扑关系仍以启发式推断为主，不适合直接生成无需人工复核的最终 SOP。

---

## 安装

```bash
pip install -r requirements.txt
```

推荐 Python 版本：

```text
Python 3.10+
```

OCR 能力依赖本地环境。若未安装 OCR 引擎，工具仍可输出基础视觉信息，但文本提取能力会受限。

---

## 快速开始

```bash
python tools/visual_extract.py examples/screenshot_error/sample_error.png --task screenshot_diagnosis --out outputs/screenshot_case
```

输出目录中会生成：

```text
visual_packet.json
visual_packet.md
annotated_regions.png
agent_instruction.md
crops/
```

其中：

* `visual_packet.json`：结构化视觉数据
* `visual_packet.md`：适合直接提供给 Agent 的 Markdown 版本
* `annotated_regions.png`：带区域标注的图片
* `agent_instruction.md`：针对任务生成的 Agent 使用指令
* `crops/`：区域裁剪图

---

## 命令参数

```bash
python tools/visual_extract.py <image> --task <task> --out <output_dir>
```

支持的任务类型：

```text
auto
screenshot_diagnosis
workflow_to_sop
ui_audit
structured_visual_reading
```

示例：

```bash
python tools/visual_extract.py ./input.png --task ui_audit --out ./outputs/ui_case
```

```bash
python tools/visual_extract.py ./workflow.png --task workflow_to_sop --out ./outputs/workflow_case
```

---

## 输出原则

Vision Harness Skill 鼓励 Agent 严格区分以下内容：

```text
事实：图中直接可见的信息
推测：基于事实和上下文做出的判断
证据：对应的 OCR 原文、区域或视觉线索
不确定点：需要人工复核的部分
动作：下一步建议
```

推荐输出结构：

```text
observed_facts
evidence_quotes
inferences
uncertainties
recommended_actions
```

---

## 项目结构

```text
vision-harness-skill/
├─ SKILL.md
├─ README.md
├─ README.zh-CN.md
├─ CHANGELOG.md
├─ requirements.txt
├─ tools/
│  ├─ visual_extract.py
│  ├─ image_loader.py
│  ├─ ocr_engine.py
│  ├─ layout_analyzer.py
│  ├─ packet_builder.py
│  └─ schema_validate.py
├─ schemas/
├─ templates/
├─ references/
├─ examples/
└─ evals/
```

---

## 当前边界

Vision Harness Skill v0.1.2 仍然是早期版本。

当前较适合：

* OCR 密集型技术截图诊断
* UI 截图的语义分析和 HTML 草稿生成
* 流程图 / 泳道图的节点和角色初步提取

当前不承诺：

* 通用图片理解
* 人脸、物体或自然场景的准确识别
* 像素级 UI 复刻
* 完整流程图拓扑恢复
* 无需人工复核的最终 SOP 生成

---

## 版本状态

当前版本：`v0.1.2`

主要改进：

* 增加 `evidence_quotes`
* 增加 `text_line_groups`
* 增强 `spatial_layout_analysis`
* 强化截图诊断模板
* 重写 workflow-to-SOP 输出约束
* 增加 UI 重构的布局树、空间约束和保真度自检

详细版本记录见 [CHANGELOG.md](CHANGELOG.md)。

---

## License

MIT
