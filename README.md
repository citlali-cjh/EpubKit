# EpubKit

一个零依赖的 EPUB 文档处理工具，支持格式转换、智能排版和电子书生成。

作者：cjh

---

## 功能特性

### 1. EPUB 转换器
将 EPUB 电子书转换为通用文本格式：
- Markdown：保留标题、列表等基本格式，便于后续编辑
- TXT：纯文本格式，兼容所有阅读设备

### 2. 智能文本格式化
针对混乱或单行文本文件的自动排版工具：
- 自动识别章节标题（如"第一章"、"Chapter 1"）
- 检测并格式化列表项（如"1.1"、"(1)"）
- 智能断句分段
- 输出结构化 Markdown 文档

### 3. EPUB 生成器
将 Markdown 或 TXT 文件转换为标准 EPUB 电子书：
- 支持自定义书名和作者信息
- 自动转换 Markdown 语法为 HTML
- 生成符合 EPUB 3.0 标准的文件
- 适用于 AI 分析后的文档再生成

---

## 使用方法

### 快速启动
Windows 用户：双击 `run.bat` 即可启动图形界面

其他平台：运行 `python EpubKit.py`

### 界面操作
软件提供三个功能标签页：

1. EPUB 转换：选择 EPUB 文件，勾选需要的输出格式，点击转换
2. 智能格式化：选择混乱的 TXT 文件，一键生成格式化的 Markdown
3. EPUB 生成：选择 MD/TXT 文件，输入书名和作者（可选），生成 EPUB

### 语言切换
界面右上角可切换中英文显示，默认为中文。

---

## 技术说明

- 开发语言：Python 3.6+
- 界面框架：Tkinter（Python 标准库）
- 依赖：无需安装任何第三方包
- 跨平台：支持 Windows、macOS、Linux

---

## 许可协议

MIT License

---

# EpubKit

A zero-dependency EPUB document processing tool supporting format conversion, intelligent formatting, and ebook generation.

Author: cjh

---

## Features

### 1. EPUB Converter
Convert EPUB ebooks to universal text formats:
- Markdown: Preserves headings and lists for further editing
- TXT: Plain text compatible with all reading devices

### 2. Smart Text Formatter
Automatic formatting tool for messy or single-line text files:
- Auto-detect chapter headers (e.g., "Chapter 1")
- Detect and format list items (e.g., "1.1", "(1)")
- Intelligent sentence and paragraph breaking
- Output structured Markdown documents

### 3. EPUB Creator
Convert Markdown or TXT files to standard EPUB ebooks:
- Customize title and author metadata
- Auto-convert Markdown syntax to HTML
- Generate EPUB 3.0 standard compliant files
- Ideal for regenerating AI-analyzed documents

---

## Usage

### Quick Start
Windows users: Double-click `run.bat` to launch the GUI

Other platforms: Run `python EpubKit.py`

### Interface
The software provides three functional tabs:

1. EPUB Converter: Select EPUB file, choose output format, convert
2. Smart Formatter: Select messy TXT file, generate formatted Markdown
3. EPUB Creator: Select MD/TXT file, enter title/author (optional), create EPUB

### Language Toggle
Switch between Chinese and English using the button in the top-right corner. Default is Chinese.

---

## Technical Details

- Language: Python 3.6+
- GUI Framework: Tkinter (Python standard library)
- Dependencies: None
- Cross-platform: Windows, macOS, Linux

---

## License

MIT License
