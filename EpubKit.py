#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EpubKit - Professional EPUB & Text Tool
Author: cjh
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import zipfile
import re
from html import unescape

# --- Localization Config ---

LANG = {
    'CN': {
        'app_title': "EpubKit - 专业文档工具",
        'tab_converter': " EPUB 转换 ",
        'tab_formatter': " 智能格式化 ",
        'header_converter': "EPUB 转 TXT / Markdown",
        'group_input': "选择文件",
        'btn_browse': "浏览...",
        'opt_txt': "生成 TXT (纯文本)",
        'opt_md': "生成 Markdown (保留格式)",
        'btn_start_convert': "开始转换",
        'header_formatter': "一键修复混乱文本",
        'desc_formatter': "自动识别章节、列表和段落，将混乱的纯文本重组为 Markdown。",
        'group_raw': "选择源文件 (.txt)",
        'btn_start_format': "格式化并保存为 MD",
        'footer': "Designed by cjh",
        'lang_switch': "English",
        'msg_no_file': "请先选择一个文件！",
        'msg_file_not_exist': "文件不存在！",
        'msg_processing': "正在处理: ",
        'msg_success_txt': "✅ TXT 导出成功",
        'msg_fail_txt': "❌ TXT 导出失败",
        'msg_success_md': "✅ Markdown 导出成功",
        'msg_fail_md': "❌ Markdown 导出失败",
        'msg_done': "完成。",
        'msg_reading': "正在读取: ",
        'msg_orig_len': "原始长度: {} 字符",
        'msg_format_success': "✅ 成功! 已保存至:\n{}",
        'msg_error_prefix': "错误: ",
        'tab_creator': " EPUB 生成 ",
        'header_creator': "Markdown/TXT 转 EPUB",
        'desc_creator': "为 AI 分析后的文档生成精美的 EPUB 电子书。",
        'group_md_input': "选择 MD/TXT 文件",
        'lbl_title': "书名:",
        'lbl_author': "作者:",
        'btn_start_create': "生成 EPUB",
        'msg_creating': "正在生成 EPUB...",
        'msg_epub_success': "✅ EPUB 生成成功!\n保存至: {}",
        'placeholder_title': "输入书名(可选)",
        'placeholder_author': "输入作者(可选)"
    },
    'EN': {
        'app_title': "EpubKit - Professional Tool",
        'tab_converter': " EPUB Converter ",
        'tab_formatter': " Smart Formatter ",
        'header_converter': "EPUB to TXT / Markdown",
        'group_input': "Input File",
        'btn_browse': "Browse...",
        'opt_txt': "Generate TXT (Plain Text)",
        'opt_md': "Generate Markdown (Formatted)",
        'btn_start_convert': "Start Conversion",
        'header_formatter': "Fix Messy Text Files",
        'desc_formatter': "Auto-detects chapters, lists, and paragraphs from messy raw text.",
        'group_raw': "Input Messy File (.txt)",
        'btn_start_format': "Format & Save as Markdown",
        'footer': "Designed by cjh",
        'lang_switch': "中文",
        'msg_no_file': "Please select a file first!",
        'msg_file_not_exist': "File does not exist!",
        'msg_processing': "Processing: ",
        'msg_success_txt': "✅ TXT Generated",
        'msg_fail_txt': "❌ TXT Failed",
        'msg_success_md': "✅ Markdown Generated",
        'msg_fail_md': "❌ Markdown failed",
        'msg_done': "Done.",
        'msg_reading': "Reading: ",
        'msg_orig_len': "Original Length: {} chars",
        'msg_format_success': "✅ Success! Saved to:\n{}",
        'msg_error_prefix': "Error: ",
        'tab_creator': " EPUB Creator ",
        'header_creator': "Markdown/TXT to EPUB",
        'desc_creator': "Generate beautiful EPUB ebooks from your AI-analyzed documents.",
        'group_md_input': "Select MD/TXT File",
        'lbl_title': "Title:",
        'lbl_author': "Author:",
        'btn_start_create': "Create EPUB",
        'msg_creating': "Creating EPUB...",
        'msg_epub_success': "✅ EPUB generated successfully!\nSaved to: {}",
        'placeholder_title': "Enter title (optional)",
        'placeholder_author': "Enter author (optional)"
    }
}

# --- Core Logic ---

def smart_format_text(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    header_patterns = [
        r'(第[一二三四五六七八九十百]+[章节部分篇][^ \n。]*)',
        r'(Chapter \d+[^ \n]*)',
        r'(Part \d+[^ \n]*)'
    ]
    for pattern in header_patterns:
        text = re.sub(pattern, r'\n\n# \1\n\n', text)
    text = re.sub(r'([。！？\n])\s*(\d+\.\d+[^ \n]*)', r'\1\n\n## \2\n\n', text)
    text = re.sub(r'([。！？\n])\s*(\d+\.|[（(]\d+[）)]|[一二三四五六七八九]\、)', r'\1\n- ', text)
    if len(text) > 1000 and text.count('\n') < 10:
        text = re.sub(r'([。！？])([^”’])', r'\1\n\n\2', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_text_from_html(html_content, keep_format=False):
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    if keep_format:
        html_content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html_content, flags=re.IGNORECASE | re.DOTALL)
        html_content = re.sub(r'<p[^>]*>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'</p>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<br[^>]*>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<hr[^>]*>', '\n---\n', html_content, flags=re.IGNORECASE)
    else:
        html_content = re.sub(r'</?(p|div|br|h[1-6]|li|tr)[^>]*>', '\n', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'<[^>]+>', '', html_content)
    html_content = unescape(html_content)
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    html_content = re.sub(r' +', ' ', html_content)
    return html_content.strip()

def get_epub_metadata(epub):
    metadata = {'title': 'Unknown', 'author': 'Unknown'}
    try:
        opf_files = [f for f in epub.namelist() if f.endswith('.opf')]
        if opf_files:
            opf_content = epub.read(opf_files[0]).decode('utf-8')
            title_match = re.search(r'<dc:title[^>]*>(.*?)</dc:title>', opf_content, re.IGNORECASE)
            if title_match: metadata['title'] = unescape(title_match.group(1).strip())
            author_match = re.search(r'<dc:creator[^>]*>(.*?)</dc:creator>', opf_content, re.IGNORECASE)
            if author_match: metadata['author'] = unescape(author_match.group(1).strip())
    except: pass
    return metadata

def epub_to_md(epub_path, output_md_path):
    try:
        with zipfile.ZipFile(epub_path, 'r') as epub:
            metadata = get_epub_metadata(epub)
            content_files = [f for f in epub.namelist() if (f.endswith('.xhtml') or f.endswith('.html')) 
                           and not f.endswith('nav.xhtml') and not f.endswith('toc.xhtml')
                           and not f.endswith('cover.xhtml')]
            content_files.sort()
            full_text = f"# {metadata['title']}\n\n**Author**: {metadata['author']}\n\n---\n\n"
            for content_file in content_files:
                try:
                    html_content = epub.read(content_file).decode('utf-8')
                    text = extract_text_from_html(html_content, keep_format=True)
                    if text.strip(): full_text += text + "\n\n"
                except: pass
            with open(output_md_path, 'w', encoding='utf-8') as f: f.write(full_text)
            return True
    except: return False

def epub_to_txt(epub_path, output_txt_path):
    try:
        with zipfile.ZipFile(epub_path, 'r') as epub:
            metadata = get_epub_metadata(epub)
            content_files = [f for f in epub.namelist() if (f.endswith('.xhtml') or f.endswith('.html')) 
                           and not f.endswith('nav.xhtml') and not f.endswith('toc.xhtml')
                           and not f.endswith('cover.xhtml')]
            content_files.sort()
            full_text = f"{metadata['title']}\nAuthor: {metadata['author']}\n" + "="*60 + "\n\n"
            for content_file in content_files:
                try:
                    html_content = epub.read(content_file).decode('utf-8')
                    text = extract_text_from_html(html_content, keep_format=False)
                    if text.strip(): full_text += text + "\n\n"
                except: pass
            with open(output_txt_path, 'w', encoding='utf-8') as f: f.write(full_text)
            return True
    except: return False

def md_to_epub(input_path, output_epub_path, title="Untitled", author="Unknown"):
    """Convert Markdown or TXT to EPUB"""
    try:
        import datetime
        import uuid
        
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to detect if it's markdown
        is_markdown = input_path.endswith('.md') or '#' in content or '**' in content
        
        # Convert MD to HTML if needed
        if is_markdown:
            # Simple MD to HTML conversion
            html_content = content
            # Headers
            html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
            # Bold and Italic
            html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
            html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
            # Lists
            html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'(<li>.*?</li>\n)+', r'<ul>\g<0></ul>', html_content, flags=re.DOTALL)
            # Paragraphs
            html_content = re.sub(r'\n\n', '</p><p>', html_content)
            html_content = '<p>' + html_content + '</p>'
            html_content = html_content.replace('<p></p>', '')
        else:
            # Plain text to HTML
            html_content = content.replace('\n', '<br/>\n')
            html_content = f'<p>{html_content}</p>'
        
        # Create EPUB structure
        uid = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # EPUB files content
        mimetype_content = 'application/epub+zip'
        
        container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''
        
        content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>{title}</dc:title>
    <dc:creator>{author}</dc:creator>
    <dc:language>en</dc:language>
    <dc:identifier id="uid">{uid}</dc:identifier>
    <meta property="dcterms:modified">{timestamp}</meta>
  </metadata>
  <manifest>
    <item id="content" href="content.xhtml" media-type="application/xhtml+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine>
    <itemref idref="content"/>
  </spine>
</package>'''
        
        content_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{title}</title>
  <style>
    body {{ font-family: sans-serif; line-height: 1.6; margin: 2em; }}
    h1 {{ color: #333; }}
    h2 {{ color: #666; }}
    p {{ margin: 1em 0; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p><strong>Author:</strong> {author}</p>
  <hr/>
  {html_content}
</body>
</html>'''
        
        nav_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>Navigation</title>
</head>
<body>
  <nav epub:type="toc">
    <h1>Table of Contents</h1>
    <ol>
      <li><a href="content.xhtml">{title}</a></li>
    </ol>
  </nav>
</body>
</html>'''
        
        # Create EPUB zip
        with zipfile.ZipFile(output_epub_path, 'w', zipfile.ZIP_DEFLATED) as epub:
            # mimetype must be first and uncompressed
            epub.writestr('mimetype', mimetype_content, compress_type=zipfile.ZIP_STORED)
            epub.writestr('META-INF/container.xml', container_xml)
            epub.writestr('OEBPS/content.opf', content_opf)
            epub.writestr('OEBPS/content.xhtml', content_xhtml)
            epub.writestr('OEBPS/nav.xhtml', nav_xhtml)
        
        return True
    except Exception as e:
        print(f"Error creating EPUB: {e}")
        return False

# --- GUI Application ---

class EpubKitApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'CN'  # Default Language
        
        self.setup_ui()
        self.update_texts()

    def setup_ui(self):
        self.root.geometry("700x550")
        
        # Styles
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Footer.TLabel", font=("Segoe UI", 8), foreground="#666666")
        
        # Top Bar (Language Switch)
        top_frame = ttk.Frame(self.root, padding="5 5 20 0")
        top_frame.pack(fill=tk.X)
        self.lang_btn = ttk.Button(top_frame, text="English", command=self.toggle_language, width=10)
        self.lang_btn.pack(side=tk.RIGHT)

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Converter
        self.tab1 = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab1, text="") # Text set dynamically
        
        self.lbl_conv_header = ttk.Label(self.tab1, text="", style="Header.TLabel")
        self.lbl_conv_header.pack(anchor=tk.W, pady=(0, 15))
        
        self.group_conv_input = ttk.LabelFrame(self.tab1, text="", padding=10)
        self.group_conv_input.pack(fill=tk.X, pady=(0, 10))
        
        self.epub_path = tk.StringVar()
        ttk.Entry(self.group_conv_input, textvariable=self.epub_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_conv_browse = ttk.Button(self.group_conv_input, text="", command=self.browse_epub)
        self.btn_conv_browse.pack(side=tk.RIGHT)
        
        opts_frame = ttk.Frame(self.tab1)
        opts_frame.pack(fill=tk.X, pady=5)
        self.do_txt = tk.BooleanVar(value=True)
        self.do_md = tk.BooleanVar(value=True)
        self.chk_txt = ttk.Checkbutton(opts_frame, text="", variable=self.do_txt)
        self.chk_txt.pack(anchor=tk.W)
        self.chk_md = ttk.Checkbutton(opts_frame, text="", variable=self.do_md)
        self.chk_md.pack(anchor=tk.W)
        
        self.btn_start_conv = ttk.Button(self.tab1, text="", command=self.run_conversion_thread)
        self.btn_start_conv.pack(fill=tk.X, pady=15)
        
        self.log_conv = scrolledtext.ScrolledText(self.tab1, height=10, state='disabled', font=("Consolas", 9))
        self.log_conv.pack(fill=tk.BOTH, expand=True)

        # Tab 2: Formatter
        self.tab2 = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab2, text="") # Text set dynamically
        
        self.lbl_fmt_header = ttk.Label(self.tab2, text="", style="Header.TLabel")
        self.lbl_fmt_header.pack(anchor=tk.W, pady=(0, 5))
        self.lbl_fmt_desc = ttk.Label(self.tab2, text="", foreground="#666")
        self.lbl_fmt_desc.pack(anchor=tk.W, pady=(0, 15))
        
        self.group_fmt_input = ttk.LabelFrame(self.tab2, text="", padding=10)
        self.group_fmt_input.pack(fill=tk.X, pady=(0, 10))
        
        self.raw_path = tk.StringVar()
        ttk.Entry(self.group_fmt_input, textvariable=self.raw_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_fmt_browse = ttk.Button(self.group_fmt_input, text="", command=self.browse_raw)
        self.btn_fmt_browse.pack(side=tk.RIGHT)
        
        self.btn_start_fmt = ttk.Button(self.tab2, text="", command=self.run_format_thread)
        self.btn_start_fmt.pack(fill=tk.X, pady=15)
        
        self.log_fmt = scrolledtext.ScrolledText(self.tab2, height=10, state='disabled', font=("Consolas", 9))
        self.log_fmt.pack(fill=tk.BOTH, expand=True)
        
        # Tab 3: EPUB Creator
        self.tab3 = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab3, text="")  # Text set dynamically
        
        self.lbl_create_header = ttk.Label(self.tab3, text="", style="Header.TLabel")
        self.lbl_create_header.pack(anchor=tk.W, pady=(0, 5))
        self.lbl_create_desc = ttk.Label(self.tab3, text="", foreground="#666")
        self.lbl_create_desc.pack(anchor=tk.W, pady=(0, 15))
        
        self.group_create_input = ttk.LabelFrame(self.tab3, text="", padding=10)
        self.group_create_input.pack(fill=tk.X, pady=(0, 10))
        
        self.md_path = tk.StringVar()
        ttk.Entry(self.group_create_input, textvariable=self.md_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.btn_create_browse = ttk.Button(self.group_create_input, text="", command=self.browse_md)
        self.btn_create_browse.pack(side=tk.RIGHT)
        
        # Metadata inputs
        meta_frame = ttk.Frame(self.tab3)
        meta_frame.pack(fill=tk.X, pady=10)
        
        self.lbl_title_text = ttk.Label(meta_frame, text="")
        self.lbl_title_text.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_var = tk.StringVar()
        self.entry_title = ttk.Entry(meta_frame, textvariable=self.title_var, width=40)
        self.entry_title.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        self.lbl_author_text = ttk.Label(meta_frame, text="")
        self.lbl_author_text.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.author_var = tk.StringVar()
        self.entry_author = ttk.Entry(meta_frame, textvariable=self.author_var, width=40)
        self.entry_author.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        meta_frame.columnconfigure(1, weight=1)
        
        self.btn_start_create = ttk.Button(self.tab3, text="", command=self.run_create_thread)
        self.btn_start_create.pack(fill=tk.X, pady=15)
        
        self.log_create = scrolledtext.ScrolledText(self.tab3, height=8, state='disabled', font=("Consolas", 9))
        self.log_create.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        self.lbl_footer = ttk.Label(self.root, text="", style="Footer.TLabel")
        self.lbl_footer.pack(pady=5)

    def toggle_language(self):
        self.current_lang = 'EN' if self.current_lang == 'CN' else 'CN'
        self.update_texts()

    def update_texts(self):
        L = LANG[self.current_lang]
        self.root.title(L['app_title'])
        self.lang_btn.config(text=L['lang_switch'])
        
        self.notebook.tab(self.tab1, text=L['tab_converter'])
        self.notebook.tab(self.tab2, text=L['tab_formatter'])
        self.notebook.tab(self.tab3, text=L['tab_creator'])
        
        self.lbl_conv_header.config(text=L['header_converter'])
        self.group_conv_input.config(text=L['group_input'])
        self.btn_conv_browse.config(text=L['btn_browse'])
        self.chk_txt.config(text=L['opt_txt'])
        self.chk_md.config(text=L['opt_md'])
        self.btn_start_conv.config(text=L['btn_start_convert'])
        
        self.lbl_fmt_header.config(text=L['header_formatter'])
        self.lbl_fmt_desc.config(text=L['desc_formatter'])
        self.group_fmt_input.config(text=L['group_raw'])
        self.btn_fmt_browse.config(text=L['btn_browse'])
        self.btn_start_fmt.config(text=L['btn_start_format'])
        
        self.lbl_create_header.config(text=L['header_creator'])
        self.lbl_create_desc.config(text=L['desc_creator'])
        self.group_create_input.config(text=L['group_md_input'])
        self.btn_create_browse.config(text=L['btn_browse'])
        self.lbl_title_text.config(text=L['lbl_title'])
        self.lbl_author_text.config(text=L['lbl_author'])
        self.btn_start_create.config(text=L['btn_start_create'])
        
        self.lbl_footer.config(text=L['footer'])

    def log(self, widget, msg):
        widget.config(state='normal')
        widget.insert(tk.END, msg + "\n")
        widget.see(tk.END)
        widget.config(state='disabled')

    def browse_epub(self):
        f = filedialog.askopenfilename(filetypes=[("EPUB Files", "*.epub")])
        if f: self.epub_path.set(f)

    def browse_raw(self):
        f = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if f: self.raw_path.set(f)

    def browse_md(self):
        f = filedialog.askopenfilename(filetypes=[("Markdown/Text", "*.md;*.txt"), ("All Files", "*.*")])
        if f: self.md_path.set(f)

    def run_conversion_thread(self):
        threading.Thread(target=self.do_convert, daemon=True).start()

    def do_convert(self):
        L = LANG[self.current_lang]
        path = self.epub_path.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", L['msg_no_file'])
            return
            
        self.log(self.log_conv, L['msg_processing'] + os.path.basename(path))
        base = os.path.splitext(path)[0]
        
        if self.do_txt.get():
            if epub_to_txt(path, base + ".txt"): self.log(self.log_conv, L['msg_success_txt'])
            else: self.log(self.log_conv, L['msg_fail_txt'])
            
        if self.do_md.get():
            if epub_to_md(path, base + ".md"): self.log(self.log_conv, L['msg_success_md'])
            else: self.log(self.log_conv, L['msg_fail_md'])
        
        self.log(self.log_conv, L['msg_done'])

    def run_format_thread(self):
        threading.Thread(target=self.do_format, daemon=True).start()

    def do_format(self):
        L = LANG[self.current_lang]
        path = self.raw_path.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", L['msg_no_file'])
            return

        self.log(self.log_fmt, L['msg_reading'] + os.path.basename(path))
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.log(self.log_fmt, L['msg_orig_len'].format(len(content)))
            formatted = smart_format_text(content)
            
            out_path = os.path.splitext(path)[0] + "_formatted.md"
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
                
            self.log(self.log_fmt, L['msg_format_success'].format(os.path.basename(out_path)))
        except Exception as e:
            self.log(self.log_fmt, L['msg_error_prefix'] + str(e))

    def run_create_thread(self):
        threading.Thread(target=self.do_create, daemon=True).start()

    def do_create(self):
        L = LANG[self.current_lang]
        path = self.md_path.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", L['msg_no_file'])
            return

        self.log(self.log_create, L['msg_creating'])
        try:
            # Get metadata
            title = self.title_var.get().strip() or os.path.splitext(os.path.basename(path))[0]
            author = self.author_var.get().strip() or "Unknown"
            
            # Generate output path
            out_path = os.path.splitext(path)[0] + ".epub"
            
            # Create EPUB
            if md_to_epub(path, out_path, title, author):
                self.log(self.log_create, L['msg_epub_success'].format(os.path.basename(out_path)))
            else:
                self.log(self.log_create, L['msg_error_prefix'] + "Failed to create EPUB")
        except Exception as e:
            self.log(self.log_create, L['msg_error_prefix'] + str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Simple CLI Mode (Always English logic for logs, but could be enhanced)
        epub_file = sys.argv[1]
        output_format = sys.argv[2] if len(sys.argv) > 2 else 'both'
        print(f"Converting {epub_file}...")
        
        base_name = os.path.splitext(epub_file)[0]
        if output_format in ['txt', 'both']: epub_to_txt(epub_file, base_name + '.txt')
        if output_format in ['md', 'both']: epub_to_md(epub_file, base_name + '.md')
        print("Done.")
    else:
        root = tk.Tk()
        w, h = 700, 550
        x = int(root.winfo_screenwidth()/2 - w/2)
        y = int(root.winfo_screenheight()/2 - h/2)
        root.geometry(f"{w}x{h}+{x}+{y}")
        app = EpubKitApp(root)
        root.mainloop()
