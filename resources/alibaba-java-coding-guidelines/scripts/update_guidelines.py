#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update the bundled Java coding guidelines markdown from the official Alibaba p3c PDF.

Pipeline:
  1. Download 《Java 开发手册（黄山版）》 PDF from alibaba/p3c (cached locally).
  2. Extract per-page text with PyMuPDF (layout preserved).
  3. Heuristically rebuild structure: headings, rule numbers, 说明/正例/反例 labels,
     Java code blocks (the PDF uses one font for body and code, so code detection is
     content-based: leading indent + syntax features), appendix tables.

Usage:
    python3 update_guidelines.py                       # download + regenerate default output
    python3 update_guidelines.py --pdf /path/to.pdf    # use a local PDF instead of downloading
    python3 update_guidelines.py --out /tmp/out.md     # custom output path

Requirements (Python >= 3.9):
    pip install pymupdf

Notes:
    - The generated markdown is the authoritative copy checked into this repo
      at references/java-coding-guidelines.md. Do not hand-edit it; regenerate.
    - Upstream license: Apache-2.0 (alibaba/p3c).
"""

import argparse
import os
import re
import sys
import tempfile
import urllib.request

PDF_URL = (
    "https://raw.githubusercontent.com/alibaba/p3c/master/"
    "Java%E5%BC%80%E5%8F%91%E6%89%8B%E5%86%8C(%E9%BB%84%E5%B1%B1%E7%89%88).pdf"
)
DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "references",
    "java-coding-guidelines.md",
)

HEADER = """# Java 开发手册（黄山版）

> **来源**：官方 PDF《Java 开发手册（黄山版）》（v1.7.1，2022-02-03 发布），取自 alibaba/p3c 仓库根目录 `Java开发手册(黄山版).pdf`；本文件为 PDF 全文转录整理。
> **协议**：Apache-2.0（与 P3C 开源 IDE 检测插件一致，见版本历史 1.3.1）。
> **维护**：本文件由 `scripts/update_guidelines.py` 从官方 PDF 自动转录生成，请勿手工编辑；如需更新请运行脚本重新生成。

## 前言
"""

# ---------------- step 1: download ----------------

def download_pdf(cache_dir):
    path = os.path.join(cache_dir, "java-dev-manual-huangshan.pdf")
    if os.path.exists(path):
        print(f"[1/3] use cached PDF: {path}")
        return path
    print(f"[1/3] downloading official PDF: {PDF_URL}")
    req = urllib.request.Request(PDF_URL, headers={"User-Agent": "update-guidelines-script"})
    with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
        f.write(r.read())
    print(f"[1/3] saved: {path} ({os.path.getsize(path)} bytes)")
    return path


# ---------------- step 2: extract ----------------

def extract_pdf(pdf_path):
    import fitz  # pymupdf

    doc = fitz.open(pdf_path)
    print(f"[2/3] extracting text, {doc.page_count} pages")
    pages = {}
    for i, page in enumerate(doc):
        pages[i + 1] = page.get_text("text", sort=True).splitlines()
    return pages


# ---------------- step 3: convert ----------------

def clean_ws(s):
    s = s.replace("\u2028", "")
    leading = len(s) - len(s.lstrip(" "))  # keep indent: code detection relies on it
    body = s.strip()
    body = re.sub(r"\s+", " ", body)
    body = re.sub(r"([\u4e00-\u9fff])\s+([\u4e00-\u9fff])", r"\1\2", body)
    body = re.sub(r"(\d+）)\s*。", r"\1", body)
    return " " * leading + body


CH_RE = re.compile(r"^[一二三四五六七]、")
SEC_RE = re.compile(r"^\(([一二三四五六七八九十]{1,3})\)\s*(.*)$")
APP_RE = re.compile(r"^附(\d+)[：:]\s*(.*)$")
RULE_RE = re.compile(r"^(\d+)\.\s*(.*)$")
SUB_RE = re.compile(r"^([0-9a-zA-Z]）)\s*(.*)$")
BUL_RE = re.compile(r"^[•⚫●·]\s*(.*)$")
LAB_RE = re.compile(r"^(说明|正例|反例)[：:]\s*(.*)$")

CODE_KEYWORDS = (
    r"public|private|protected|class|interface|enum|void|int|long|short|byte|char|"
    r"float|double|boolean|String|final|import|package|return|new|if|for|while|"
    r"switch|case|catch|throw|try|extends|implements|static|synchronized|assert|"
    r"this|super|else|default|break|continue|instanceof"
)


def is_code(s):
    indent = len(s) - len(s.lstrip(" "))
    st = s.strip()
    if indent < 2:
        return False
    if re.search(r"[;{}]", st):
        return True
    if "//" in st:
        return True
    if re.match(r"^(?:" + CODE_KEYWORDS + r")\b", st):
        return True
    if st.startswith("@") and re.match(r"^@[a-zA-Z_$][\w$]*", st):
        return True
    if re.search(r"->|::", st):
        return True
    if re.match(r"^[a-zA-Z_$][\w$<>\[\].]*\s*[=(]\s*", st) and not re.search(
        r"[\u4e00-\u9fff]", st.split("(")[0]
    ):
        return True
    return False


def build_version_table():
    return """| 版本号 | 版本名 | 发布日期 | 备注 |
| --- | --- | --- | --- |
| -- | -- | 2016.12.07 | 试读版本首次对外发布 |
| 1.0.0 | 正式版 | 2017.02.09 | 阿里巴巴集团正式对外发布 |
| 1.0.1 | -- | 2017.02.13 | 1）修正String[]的前后矛盾；2）vm修正成velocity；3）修正countdown描述错误 |
| 1.0.2 | -- | 2017.02.20 | 1）去除文底水印；2）数据类型中引用太阳系年龄问题；3）修正关于异常和方法签名的部分描述；4）修正final描述；5）去除Comparator部分描述 |
| 1.1.0 | -- | 2017.02.27 | 1）增加前言；2）增加<? extends T>描述和说明；3）增加版本历史；4）增加专有名词解释 |
| 1.1.1 | -- | 2017.03.31 | 修正页码总数和部分示例 |
| 1.2.0 | 完美版 | 2017.05.20 | 1）根据云栖社区的“聚能聊”活动反馈，对手册的页码、排版、描述进行修正；2）增加final的适用场景描述；3）增加关于锁的粒度的说明；4）增加“指定集合大小”的详细说明以及正反例；5）增加卫语句的示例代码；6）明确数据库表示删除概念的字段名为is_deleted |
| 1.3.0 | 终极版 | 2017.09.25 | 增加单元测试规约，阿里开源的IDE代码规约检测插件：[点此下载](https://github.com/alibaba/p3c) |
| 1.3.1 | 纪念版 | 2017.11.30 | 修正部分描述；采用和P3C开源IDE检测插件相同的Apache2.0协议 |
| 1.4.0 | 详尽版 | 2018.05.20 | 增加设计规约大类，共16条 |
| 1.5.0 | 华山版 | 2019.06.19 | 1）鉴于手册是Java社区开发者集体智慧的结晶，移除限定词“阿里巴巴”；2）新增21条新规约；3）修改描述112处；4）完善若干处示例 |
| 1.6.0 | 泰山版 | 2020.04.22 | 1）发布错误码统一解决方案，详细参考附表3；2）修改描述90处；3）完善若干处示例；4）新增34条新规约 |
| 1.7.0 | 嵩山版 | 2020.08.03 | 1）新增前后端规约14条；2）新增禁止任何歧视性用语的约定；3）新增涉及敏感操作的情况下日志需要保存六个月的约定；4）修正BigDecimal类中关于compareTo和equals的等值比较；5）修正HashMap关于1024个元素扩容的次数；6）修正架构分层规范与相关说明；7）修正泰山版中部分格式错误和描述错误 |
| 1.7.1 | 黄山版 | 2022.02.03 | 1）新增11条新规约；2）新增描述中的正反例2条，新增扩展说明5条；3）修改描述22处；4）修正嵩山版中部分代码格式错误和描述错误 |"""


def build_error_table(pages):
    err_rows = []
    for p in range(48, 55):  # error-code appendix spans pages 48..55 in v1.7.1
        for raw in pages.get(p, []):
            s = raw.strip()
            if not s or s == "Java 开发手册（黄山版）":
                continue
            if re.fullmatch(r"\d+/\d+", s) or s.startswith("错误码") or s.startswith("附3"):
                continue
            m = re.match(r"^(\S+)\s+(.*)$", s)
            if not m:
                continue
            code = m.group(1)
            rest = m.group(2)
            if re.search(r"[\u4e00-\u9fff]", code):
                continue
            parts = re.split(r"\s{3,}", rest)
            desc = clean_ws(parts[0]) if parts else ""
            note = clean_ws(parts[1]) if len(parts) > 1 else ""
            if desc:
                err_rows.append((code, desc, note))
    lines = ["| 错误码 | 中文描述 | 说明 |", "| --- | --- | --- |"]
    for code, desc, note in err_rows:
        lines.append(f"| {code} | {desc} | {note} |")
    return "\n".join(lines)


def convert(pages):
    # line stream: drop cover/version-history lead-in, keep body from 前言 onward
    lines = []
    started = False
    for p in range(2, 55):
        if p in (1, 3, 55):
            continue
        for raw in pages.get(p, []):
            s = clean_ws(raw)
            st = s.strip()
            if not st or st == "Java 开发手册（黄山版）":
                continue
            if re.fullmatch(r"\d+/\d+", st):
                continue
            if p == 2:  # 前言 page: keep whole
                lines.append(s)
                continue
            if not started:
                if CH_RE.match(s):
                    started = True
                else:
                    continue
            lines.append(s)

    version_table = build_version_table()
    error_table = build_error_table(pages)

    blocks = []
    in_code = False

    def flush_code():
        nonlocal in_code
        if in_code:
            blocks.append(("code_end", ""))
            in_code = False

    skip_zone = None
    for s in lines:
        st = s.strip()
        if skip_zone == "v1" and not re.match(r"^附2[：:]", st):
            continue
        if skip_zone == "v3":
            continue
        m = APP_RE.match(st)
        if m:
            flush_code()
            if m.group(1) == "1":
                blocks.append(("h2", "附1：版本历史"))
                blocks.append(("table", version_table))
                skip_zone = "v1"
            elif m.group(1) == "2":
                blocks.append(("h2", "附2：专有名词解释"))
                skip_zone = "v2"
            elif m.group(1) == "3":
                blocks.append(("h2", "附3：错误码列表"))
                blocks.append(("table", error_table))
                skip_zone = "v3"
            continue
        if st == "前言":
            # HEADER already carries the 前言 heading; drop the PDF line
            continue
        if re.match(r"^[一二三四五六七]、", st):
            flush_code()
            blocks.append(("h2", st))
            continue
        m = SEC_RE.match(st)
        if m:
            flush_code()
            blocks.append(("h3", f"（{m.group(1)}）{m.group(2)}"))
            continue
        m = RULE_RE.match(st)
        if m:
            flush_code()
            blocks.append(("rule", st))
            continue
        m = BUL_RE.match(st)
        if m:
            flush_code()
            blocks.append(("bullet", m.group(1)))
            continue
        m = SUB_RE.match(st)
        if m:
            flush_code()
            blocks.append(("plain", st))
            continue
        m = LAB_RE.match(st)
        if m:
            flush_code()
            blocks.append(("label", f"**{m.group(1)}**：{m.group(2)}"))
            continue
        if is_code(s):
            if not in_code:
                blocks.append(("code_start", ""))
                in_code = True
            blocks.append(("code", s))
            continue
        if in_code:
            flush_code()
        if blocks and blocks[-1][0] in ("rule", "plain", "bullet", "label", "prose"):
            t, prev = blocks[-1]
            blocks[-1] = (t, prev + st)
        else:
            blocks.append(("prose", st))

    if in_code:
        blocks.append(("code_end", ""))

    out = [HEADER]
    for t, text in blocks:
        if t == "code_start":
            out.append("```java")
        elif t == "code_end":
            out.append("```")
        elif t == "code":
            out.append(text)
        elif t == "h2":
            out += ["", f"## {text}", ""]
        elif t == "h3":
            out += ["", f"### {text}", ""]
        elif t == "table":
            out += ["", text, ""]
        elif t == "bullet":
            if out and out[-1].startswith("- "):
                out.append(f"- {text}")
            else:
                out += ["", f"- {text}"]
        elif t == "rule":
            out += ["", text, ""]
        elif t == "plain":
            out += ["", text, ""]
        elif t == "label":
            out += ["", text, ""]
        elif t == "prose":
            out += ["", text, ""]

    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return body


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", help="path to a local PDF; omit to download the official one")
    ap.add_argument("--out", default=DEFAULT_OUT, help=f"output markdown (default: {DEFAULT_OUT})")
    ap.add_argument("--cache-dir", default=tempfile.gettempdir(), help="download cache dir")
    args = ap.parse_args()

    if args.pdf:
        pdf_path = args.pdf
        print(f"[1/3] use provided PDF: {pdf_path}")
    else:
        pdf_path = download_pdf(args.cache_dir)

    pages = extract_pdf(pdf_path)
    body = convert(pages)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(body)

    n_force = len(re.findall(r"【强制】", body))
    n_rec = len(re.findall(r"【推荐】", body))
    n_ref = len(re.findall(r"【参考】", body))
    n_code = body.count("```") // 2
    print(f"[3/3] written: {args.out} ({len(body)} bytes, {len(body.splitlines())} lines)")
    print(f"      rules: 强制={n_force} 推荐={n_rec} 参考={n_ref}, code blocks={n_code}")


if __name__ == "__main__":
    sys.exit(main())
