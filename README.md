# Vision Harness Skill

[English README](README.en.md)

Vision Harness Skill 是一个面向 Agent 的结构化视觉理解技能包。

它有两个目标：

1. **让文字类大语言模型 Agent 能“看见图”。** 它会把图片转换成结构化的 `visual_packet`，让没有原生视觉能力的 Agent 可以基于文字识别结果、版面区域、视觉特征、路由建议和不确定性说明进行推理。
2. **让多模态大语言模型 Agent 能“看好图”。** 它为多模态 Agent 提供结构化读图协议，强制区分观察事实、推测结论、证据区域、不确定点和后续动作。

这个项目不是另一个多模态模型。它是一个围绕 Agent 的视觉理解控制层。

---

## 为什么需要这个项目

原生多模态模型可以描述图片，但 Agent 工作流通常需要更严格的结果：

- 需要证据区域，而不是模糊判断；
- 需要区分事实和推测；
- 需要明确标注不确定点；
- 需要机器可读的 JSON；
- 需要截图诊断；
- 需要把流程图转成标准操作流程；
- 需要对界面截图做有优先级的评审；
- 需要给没有视觉能力的文字类 Agent 提供保底输入。

Vision Harness Skill 的目标是把自由发挥式的图片分析，变成可复用、可复核、可执行的 Agent 工作流。

---

## v0.1 包含什么

- 面向 Claude Code、Codex 及类似 Agent 的 `SKILL.md`；
- 用于生成 `visual_packet` 的 `tools/visual_extract.py`；
- 可选的文字识别支持；
- 带编号区域的标注图生成；
- Markdown 和 JSON 两种视觉语义包输出；
- 三个任务模板：
  - 截图诊断；
  - 流程图转标准操作流程；
  - 界面截图评审；
- JSON 结构定义；
- 常见误区和安全边界说明；
- 轻量评估脚手架。

---

## 项目结构

```text
vision-harness-skill/
├─ SKILL.md
├─ README.md
├─ README.en.md
├─ requirements.txt
├─ tools/
│  ├─ visual_extract.py
│  ├─ image_loader.py
│  ├─ ocr_engine.py
│  ├─ layout_analyzer.py
│  ├─ region_marker.py
│  ├─ packet_builder.py
│  └─ schema_validate.py
├─ schemas/
├─ templates/
├─ references/
├─ examples/
└─ evals/
```

---

## 安装

安装最小依赖：

```bash
pip install -r requirements.txt
```

可选安装文字识别引擎：

```bash
pip install rapidocr-onnxruntime
```

或者：

```bash
pip install pytesseract
```

如果没有安装文字识别引擎，工具仍然可以运行，但 `ocr_blocks` 会为空。

---

## 快速开始

```bash
python tools/visual_extract.py examples/screenshot_error/sample_error.png --task screenshot_diagnosis --out outputs/screenshot_case
```

预期输出：

```text
outputs/screenshot_case/
├─ visual_packet.json
├─ visual_packet.md
├─ annotated_regions.png
├─ agent_instruction.md
└─ crops/
```

---

## 模式一：文字类 Agent 模式

当 Agent 不能直接查看图片时，使用这个模式。

先运行提取工具：

```bash
python tools/visual_extract.py input.png --task auto --out outputs/case1
```

然后把以下材料交给文字类大语言模型 Agent：

- `visual_packet.md` 或 `visual_packet.json`；
- `templates/text_agent_mode.md`；
- `visual_packet` 中推荐的任务模板。

Agent 必须说明：它是在基于图片转译结果推理，而不是直接看到了原图。

---

## 模式二：多模态 Agent 模式

当 Agent 本身已经能查看图片，但需要更严格的视觉推理流程时，使用这个模式。

把以下材料交给多模态 Agent：

- 原始图片；
- `annotated_regions.png`；
- `visual_packet.json` 或 `visual_packet.md`；
- `templates/multimodal_agent_mode.md`；
- 对应任务模板。

Agent 必须引用区域编号，并且区分事实和推测。

---

## 任务模板

| 任务 | 适用场景 | 模板 |
|---|---|---|
| 截图诊断 | 报错截图、软件问题、界面错误提示、监控看板 | `templates/screenshot_diagnosis.md` |
| 流程图转标准操作流程 | 流程图、白板流程、业务流程图、泳道图 | `templates/workflow_to_sop.md` |
| 界面截图评审 | 产品截图、网页或应用界面、用户体验评审、信息架构检查 | `templates/ui_audit.md` |

---

## 输出纪律示例

不好的输出：

> 这个截图显示有严重的后端问题。

更好的输出：

```json
{
  "observed_facts": [
    "文字块 text_001 包含 '502 Bad Gateway'。",
    "疑似错误信息位于 region_005 附近。"
  ],
  "inferences": [
    "页面可能在网关或反向代理层出现失败。"
  ],
  "evidence_regions": ["region_005", "text_001"],
  "next_checks": [
    "检查截图时间附近的反向代理日志。",
    "确认上游服务健康状态和超时配置。"
  ],
  "uncertainties": [
    "仅凭截图不能确定根因。"
  ]
}
```

---

## 设计原则

- 脚本负责确定性提取。
- 大语言模型负责推理。
- Skill 文件提供方法、常见误区、结构定义和任务模板。
- 重要判断必须有证据。
- 不确定性是输出的一部分，不是失败。
- 文字类 Agent 模式不能假装自己拥有原生视觉能力。
- 多模态 Agent 模式不能跳过证据直接下结论。

---

## 能力边界

v0.1 不做以下事情：

- 不训练或内置视觉模型；
- 不把多模态模型作为语义观察者；
- 不执行电脑点击操作；
- 不保证文字识别完全准确；
- 不保证准确解析所有流程图连线；
- 不抽取精确图表数值；
- 不支持医学、法律、安全、身份识别或监控等高风险判断。

---

## 许可证

MIT
