# OCR2Markdown — vLLM 方案失败分析与备选记录

## 目标

在 Modal L4 GPU 容器内，通过 MinerU Python API 调用 vLLM engine backend，实现真正的 GPU 并行处理多个 PDF。

## 方案设计

```python
from mineru.backend.vlm.vlm_analyze import ModelSingleton

# 同步阻塞加载 vLLM 模型
model = ModelSingleton().get_model(
    backend="vllm-engine",
    model_path=None,
    server_url=None,
)
print("Model ready!")

# 批量处理
for pdf_path in pdf_files:
    images = _pdf_to_images(pdf_path)
    results = model.batch_two_step_extract(images)  # <-- 这里报错
```

Modal 镜像使用 `vllm/vllm-openai:v0.11.2` 基础镜像。

## 错误现象

调用 `model.batch_two_step_extract(images)` 时，MinerU 内部抛出异常：

```
ERROR: division by zero
```

错误堆栈指向 `mineru` 内部 `append_page_blocks_to_middle_json` 相关逻辑。所有 4 个测试 PDF（book_1, inbox_1-3）均报此错误。

## 根因分析

**初步判断**：这是 MinerU 内部的 bug，与 backend 选择（huggingface / vllm-engine）无关。

- 4 个 PDF 全部报错，排除 PDF 内容特殊性
- CLI 的 `mineru -p <pdf> -o <out> -b pipeline` 能正常处理，说明模型权重和依赖本身没问题
- Python API 和 CLI 都调用同一套模型推理代码，只是调用路径不同
- `division by zero` 发生在结果后处理（JSON 拼接）阶段，而非 GPU 推理阶段

## 备选方案

### 方案 A：CLI subprocess（当前采用）

```python
res = subprocess.run(
    ["mineru", "-p", str(pdf_path), "-o", str(work_dir), "-b", "pipeline"],
    capture_output=True,
    text=True,
)
```

**优点**：能正常工作，`-b pipeline` 模式稳定
**缺点**：
- 串行执行，一个接一个
- 每次调用重新初始化模型（~30s cold start）
- GPU 利用率受限于 CPU/pdf 解析速度

### 方案 B：vLLM HTTP server（未尝试）

启动 vLLM server 后通过 HTTP API 调用。理论上可复用模型实例，但需要额外进程管理和 server lifecycle。复杂度高，vLLM server 和 MinerU 的 API 兼容也需要适配。

### 方案 C：多容器并行（测试过但有问题）

利用 Modal 的 `function.remote()` 特性，每个 PDF 调度到独立容器并行处理。但测试中发现 volume mount 在 `.remote()` 子调用中行为异常（PDF 枚举找不到文件），未完全调通。

## 当前状态

- **采用**：CLI subprocess 方案（`mineru -b pipeline`）
- **运行方式**：`modal run ./src/ocr2markdown.py --slug <slug>`
- **处理流程**：串行，逐个处理 volume upload/ 目录下的所有 PDF
- **跳过逻辑**：已处理过的 PDF（output 目录存在 .md 文件）自动跳过

## 待修复

1. **调查 vLLM Python API division by zero** — 需要在 mineru 源码层面找到触发条件，看是否是特定 PDF 结构导致
2. **尝试 vLLM HTTP server 方案** — 绕过 Python API 的 JSON 处理问题
3. **多容器并行** — 如果需要加速，可重新调研 Modal 多容器调度时的 volume mount 行为

## 参考

- MinerU 官方文档：https://opendatalab.github.io/MinerU/
- vLLM engine backend：https://github.com/vllm-project/vllm
- 原始计划：`docs/plan.ocr2markdown.vllm.md`
