# IndexTTS2 命令行工具使用说明

## 📋 目录

- [简介](#简介)
- [环境要求](#环境要求)
- [工具说明](#工具说明)
- [使用方法](#使用方法)
  - [单文件克隆](#单文件克隆)
  - [批量克隆](#批量克隆)
- [文件命名规则](#文件命名规则)
- [常见问题](#常见问题)

---

## 简介

本工具提供两个命令行脚本，用于 IndexTTS2 语音克隆，无需 WebUI 界面：

- **`tts_cli.py`** - 单文件语音克隆
- **`batch_clone.py`** - 批量文件夹语音克隆

---

## 环境要求

- Python 3.10+
- 已安装依赖：`uv sync` 或使用虚拟环境 `.venv`
- 模型文件位于 `checkpoints/` 目录

---

## 工具说明

### 1. `tts_cli.py` - 单文件克隆

用于克隆单个音频文件的音色，并合成指定文本。

**特点：**
- 快速生成单个音频
- 支持情感参考音频
- 适合测试和单次使用

### 2. `batch_clone.py` - 批量克隆

用于批量处理文件夹中的所有 `.wav` 文件。

**特点：**
- 自动遍历文件夹
- 从文件名提取文本内容
- 智能处理序号前缀
- 输出到 `cn/` 子文件夹
- 显示处理进度

---

## 使用方法

### 单文件克隆

#### 基本用法

```bash
cd /Users/linkunkun/Documents/AI_Tools/voice_clone/index-tts

# 使用虚拟环境
.venv/bin/python tts_cli.py \
  --speaker examples/voice_01.wav \
  --text "你好，这是一个测试。" \
  --output output.wav
```

#### 完整参数

```bash
.venv/bin/python tts_cli.py \
  --speaker examples/voice_01.wav \        # 说话人音频（克隆音色）
  --text "你好世界" \                      # 要合成的文本
  --output my_audio.wav \                  # 输出文件名
  --emotion-audio examples/emo_happy.wav \ # (可选) 情感参考音频
  --model-dir checkpoints \                # (可选) 模型目录
  --cfg-path checkpoints/config.yaml       # (可选) 配置文件
```

#### 简短用法

```bash
.venv/bin/python tts_cli.py -s voice.wav -t "你好" -o out.wav
```

---

### 批量克隆

#### 基本用法（推荐）

```bash
cd /Users/linkunkun/Documents/AI_Tools/voice_clone/index-tts

# 输出自动保存到 input_folder/cn/ 目录
.venv/bin/python batch_clone.py --input ./my_audio_folder
```

#### 自定义输出目录

```bash
.venv/bin/python batch_clone.py \
  --input ./input_wavs \
  --output ./custom_output
```

#### 完整参数

```bash
.venv/bin/python batch_clone.py \
  --input ./my_audio \              # 输入文件夹（必需）
  --output ./output_folder \        # 输出文件夹（可选，默认为 input/cn/）
  --model-dir checkpoints \         # 模型目录（可选）
  --cfg-path checkpoints/config.yaml # 配置文件（可选）
```

---

## 文件命名规则

### 批量克隆的命名规则

批量克隆会自动从文件名提取文本内容，智能去除序号前缀：

| 输入文件名 | 提取的文本 | 输出文件名 |
|-----------|-----------|-----------|
| `1 how old are you.wav` | `how old are you` | `1 how old are you.wav` |
| `1-how old are you.wav` | `how old are you` | `1-how old are you.wav` |
| `15-你好世界.wav` | `你好世界` | `15-你好世界.wav` |
| `2_测试音频.wav` | `测试音频` | `2_测试音频.wav` |

**支持的序号格式：**
- `数字 + 空格`：`1 text.wav`
- `数字 + 横线`：`1-text.wav`
- `数字 + 下划线`：`1_text.wav`
- 纯数字：`1text.wav` → `text.wav`

---

## 使用示例

### 示例 1：快速测试

```bash
cd /Users/linkunkun/Documents/AI_Tools/voice_clone/index-tts

# 使用示例音频进行测试
.venv/bin/python tts_cli.py \
  -s examples/voice_01.wav \
  -t "大家好，我是 AI 语音助手。" \
  -o test.wav
```

### 示例 2：批量处理项目文件

假设你有一个文件夹结构：
```
my_project/
├── 1-你好世界.wav
├── 2-今天天气真好.wav
├── 3-我喜欢编程.wav
└── ...
```

运行批量处理：
```bash
.venv/bin/python batch_clone.py --input ./my_project
```

输出结果：
```
my_project/
├── 1-你好世界.wav              (原文件)
├── 2-今天天气真好.wav          (原文件)
├── 3-我喜欢编程.wav            (原文件)
└── cn/                         (自动创建)
    ├── 1-你好世界.wav          (克隆后的音频)
    ├── 2-今天天气真好.wav      (克隆后的音频)
    └── 3-我喜欢编程.wav        (克隆后的音频)
```

### 示例 3：使用情感控制

```bash
.venv/bin/python tts_cli.py \
  --speaker examples/voice_12.wav \
  --text "快躲起来！他要来了！" \
  --emotion-audio examples/emo_sad.wav \
  --output emotional_speech.wav
```

---

## 常见问题

### Q1: 模型加载很慢怎么办？

**A:** 第一次加载模型需要时间（约 30-60 秒），之后会缓存到内存。批量处理时，模型只加载一次，处理多个文件会很快。

### Q2: 如何查看处理进度？

**A:** 批量克隆工具会显示进度条：
```
🎙️ 处理进度: 45%|████▌     | 9/20 [02:15<02:45, 15.05s/文件]
```

### Q3: 输出文件在哪里？

**A:** 
- **单文件克隆**：在 `--output` 指定的位置
- **批量克隆**：默认在输入文件夹的 `cn/` 子目录下

### Q4: 支持哪些音频格式？

**A:** 
- **输入**：`.wav` 文件（16kHz 或 22kHz 采样率）
- **输出**：`.wav` 文件（22kHz 采样率）

### Q5: 处理失败怎么办？

**A:** 批量处理会显示失败的文件和错误信息，成功的文件不受影响。常见原因：
- 文件名无法提取文本（全是数字）
- 音频文件损坏
- 文本过长（建议不超过 200 个字符）

### Q6: 如何停止批量处理？

**A:** 按 `Ctrl + C` 可以随时中断处理。已处理的文件会保存。

### Q7: 警告信息需要处理吗？

**A:** 以下警告可以忽略，不影响功能：
```
GPT2InferenceModel has generative capabilities...
Passing a tuple of `past_key_values` is deprecated...
```

### Q8: 如何提高处理速度？

**A:** 
- 使用 GPU 加速（如果有）
- 减少文本长度
- 关闭详细输出（`verbose=False`）

### Q9: 可以处理英文吗？

**A:** 可以！IndexTTS2 支持中英文混合：
```bash
.venv/bin/python tts_cli.py \
  -s voice.wav \
  -t "Hello world, 你好世界！" \
  -o bilingual.wav
```

---

## 快速参考

### 单文件克隆
```bash
.venv/bin/python tts_cli.py -s 音色.wav -t "文本" -o 输出.wav
```

### 批量克隆
```bash
.venv/bin/python batch_clone.py -i 输入文件夹
```

### 查看帮助
```bash
.venv/bin/python tts_cli.py --help
.venv/bin/python batch_clone.py --help
```

---

## 技术支持

- **项目地址**: https://github.com/index-tts/index-tts
- **文档**: [README.md](README.md)
- **问题反馈**: 在 GitHub Issues 中提交

---

## 更新日志

### v1.0 (2025-10-24)
- ✅ 创建命令行工具
- ✅ 支持单文件和批量克隆
- ✅ 自动文件名处理
- ✅ 默认输出到 cn/ 文件夹
- ✅ 进度条显示

---

**祝使用愉快！🎉**

