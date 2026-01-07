# EpubKit 使用指南

## 项目介绍

EpubKit 是一个**多功能**文档处理工具，专注于解决电子书和文档格式转换的痛点。它不仅是一个轻量级的 EPUB 转换器，还内置了**智能文本格式化引擎**，能够将混乱的纯文本（如只有一行的 TXT）自动重组为结构清晰的文档。

**作者**: cjh

---

## 核心功能

### 1. EPUB 转换器 (EPUB Converter)
无需安装庞大的软件，即可将 `.epub` 电子书转换为通用格式：
- **Markdown**: 保留标题、粗体、列表等排版，适合导入笔记软件（Obsidian/Notion）。
- **TXT**: 纯净文本，适合在任何设备上阅读。

### 2. 智能格式化 (Smart Formatter)
这是本项目最独特的功能。针对那种"全书只有一行"或者"排版混乱"的 TXT 文件，EpubKit 能自动识别：
- 章节标题 (如 "第一章", "Chapter 1")
- 序号列表 (如 "1.1", "(1)")
- 段落结构
并将它们自动重排为漂亮的 Markdown 文档。

---

## 使用说明

### 下载与安装
本项目完全基于 Python 原生库开发，**零依赖**，无需安装任何额外包。
- 如果你是开发者：直接运行 `python EpubKit.py`
- 如果你是普通用户：双击 `run.bat`

### 界面操作
1. **启动软件**: 双击 `run.bat`，看到现代化的操作界面。
2. **转换电子书**:
   - 点击 "EPUB Converter" 标签页。
   - 选择你的 EPUB 文件。
   - 点击 "Start Conversion"。
3. **修复乱码/单行文本**:
   - 点击 "Smart Formatter" 标签页。
   - 选择那个很难读的 TXT 文件。
   - 点击 "Format & Save"，软件会自动分析并生成一个新的 `.md` 文件。

---

# EpubKit - Documentation

## Introduction

EpubKit is a versatile document processing tool designed to solve common ebook and document formatting issues. It acts as both a lightweight EPUB converter and an **Intelligent Text Formatter**, capable of restructuring messy plain text files (e.g., single-line TXTs) into well-organized documents.

**Author**: cjh

---

## Features

### 1. EPUB Converter
Convert `.epub` ebooks into universal formats without heavy dependencies:
- **Markdown**: Preserves headings, bold text, and lists. Perfect for note-taking apps.
- **TXT**: Clean plain text for universal compatibility.

### 2. Smart Formatter
The flagship feature of this project. For TXT files that are "one giant line" or poorly formatted, EpubKit automatically detects:
- Chapter Headers (e.g., "Chapter 1")
- Numbered Lists (e.g., "1.1")
- Paragraph Breaks
It then reconstructs the text into a clean, readable Markdown document.

---

## Usage

### Installation
Built with pure Python standard libraries. **Zero Dependencies**.
- **Developers**: Run `python EpubKit.py`
- **Users**: Double-click `run.bat`

### How to use
1. **Launch**: Double-click `run.bat` to open the GUI.
2. **Convert EPUB**:
   - Go to "EPUB Converter" tab.
   - Select your EPUB file.
   - Click "Start Conversion".
3. **Fix Messy Text**:
   - Go to "Smart Formatter" tab.
   - Select your messy TXT file.
   - Click "Format & Save". The tool will analyze and save a formatted `.md` file.

---
MIT License
