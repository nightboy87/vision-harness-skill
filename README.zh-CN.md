# Vision Harness Skill

[English README](README.md)

Vision Harness Skill 是一个面向 Agent 的结构化视觉理解技能包。

它有两个目标：

1. **让文字类大语言模型 Agent 能“看见图”。** 它会把图片转换成结构化的 `visual_packet`，让没有原生视觉能力的 Agent 可以基于 OCR 文本块、证据原文、文本行分组、版面区域、视觉特征、路由建议和不确定性说明进行推理。
2. **让多模态大语言模型 Agent 能“看好图”。** 它为多模态 Agent 提供结构化读图协议，强制区分观察事实、推测结论、证据区域、证据原文、不确定点和后续动作。

这个项目不是另一个多模态模型。它是一个围绕 Agent 的视觉理解控制层。

---

## v0.1.2 更新内容

v0.1.2 基于三个真实场景测试优化：

- 高文字密度技术截图诊断；
- 泳道流程图结构化；
- UI 截图分析与 HTML 复刻。

主要改进：

- 新增 `evidence_quotes`，关键 OCR 判断必须能引用原文或归一化文本；
- 新增 `text_line_groups`，更适合日志、表格、仪表盘和 UI 文本簇；
- 新增启发式 `spatial_layout_analysis`，用于识别侧边栏、右侧信息栏、底部状态栏、泳道/网格候选等空间信号；
- 强化截图诊断规则：禁止模板污染，禁止把局部成功当整体成功，强化事实/推测分离；
- 重写流程图转 SOP 模板：拆分为原图提取 SOP、业务推测解释、建议补充内容；
- 流程图决策点必须有显式证据，不能凭业务常识生成；
- 重写 UI 模板，区分 `ui_audit`、`ui_semantic_rebuild`、`ui_fidelity_clone`；
- 新增 UI 布局树、空间约束和保真度自检规则。

---

## 当前最适合的场景

最适合：

1. 高文字密度技术截图诊断；
2. UI 截图分析与语义级 HTML 重构；
3. 流程图初步结构化与 SOP 草稿生成。

暂不适合：

1. 像素级 UI 高保真复刻；
2. 全自动流程图拓扑恢复；
3. 无人工复核的最终 SOP 生成；
4. 医学、法律、安全、身份识别、监控等高风险判断。

---

## 为什么需要这个项目

原生多模态模型可以描述图片，但 Agent 工作流通常需要更严格的结果：

- 需要证据区域，而不是模糊判断；
- 需要证据原文，而不是只有 text ID；
- 需要区分事实和推测；
- 需要明确标注不确定点；
- 需要机器可读的 JSON；
- 需要截图诊断；
- 需要把流程图转成标准操作流程草稿；
- 需要对界面截图做评审或复刻约束；
- 需要给没有视觉能力的文字类 Agent 提供保底输入。

Vision Harness Skill 的目标是把自由发挥式的图片分析，变成可复用、可复核、可执行的 Agent 工作流。

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

可选安装 OCR 引擎。中文 UI、流程图和截图建议优先尝试：

```bash
pip install paddleocr
```

或者使用较轻量的 OCR 选项：

```bash
pip install rapidocr-onnxruntime
```

也可以使用：

```bash
pip install pytesseract
```

如果没有安装 OCR 引擎，工具仍然可以运行，但 `ocr_blocks` 会为空。

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

Agent 必须引用区域编号；如果结论依赖文字，还要引用证据原文；同时必须区分事实和推测。

---

## 任务模板

| 任务 | 适用场景 | 模板 |
|---|---|---|
| 截图诊断 | 报错截图、构建日志、软件问题、界面错误提示、监控看板 | `templates/screenshot_diagnosis.md` |
| 流程图转 SOP | 流程图、白板流程、业务流程图、泳道图 | `templates/workflow_to_sop.md` |
| UI 评审 / 复刻 | 产品截图、网页或应用界面、UX 评审、UI 语义重构、UI 保真复刻 | `templates/ui_audit.md` |

---

## 设计原则

- 脚本负责确定性提取。
- 大语言模型负责推理和生成。
- Skill 文件提供方法、常见误区、结构定义和任务模板。
- 重要判断必须有证据。
- 依赖文字的关键判断应该尽量引用 OCR 原文或归一化文本。
- 不确定性是输出的一部分，不是失败。
- 文字类 Agent 模式不能假装自己拥有原生视觉能力。
- 多模态 Agent 模式不能跳过证据直接下结论。

---

## 能力边界

v0.1.2 不做以下事情：

- 不训练或内置视觉模型；
- 不把多模态模型作为语义观察者；
- 不执行电脑点击操作；
- 不保证 OCR 完全准确；
- 不保证准确解析所有流程图连线；
- 不抽取精确图表数值；
- 不保证像素级 HTML/CSS 复刻；
- 不支持医学、法律、安全、身份识别或监控等高风险判断。

---

## 推荐开发流程

1. 用真实图片运行 `visual_extract.py`。
2. 检查 `visual_packet.md` 和 `annotated_regions.png`。
3. 让文字类或多模态 Agent 使用推荐模板。
4. 检查回答是否区分事实、推测、证据、不确定点和动作。
5. 出现失败案例后，优先补充 gotchas 和模板规则，再考虑改工具。
