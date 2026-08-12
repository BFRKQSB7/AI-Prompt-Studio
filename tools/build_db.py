#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从「AI 绘画提示词超市」HTML 生成转换器用的提示词检索库。

产出:
  prompt-db.js   全量库: const PROMPT_DB=[["中文","英文"],...]  (类型0通用+3系列+4角色, 含中文, 去重)
  curated-lib.js 精选库: const CURATED_LIB=[["中文","英文"],...] (CURATED 人工精选分类 + 补充词)

用法:
  python tools/build_db.py [超市HTML路径] --db-out prompt-db.js --curated-out curated-lib.js
默认超市路径: E:\\AI\\ai-image\\AI 绘画提示词超市.html
"""
import argparse
import json
import os
import re
import sys


def read_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_obj(data, const_name):
    """返回 const <name> = {...} 对象文本（排除注释里的 `= {...}`）。"""
    pat = re.compile(re.escape("const " + const_name) + r"\s*=\s*\{")
    for m in pat.finditer(data):
        i = m.start()
        if data.startswith("const " + const_name + " = {...", i):
            continue
        depth = 0
        j = i
        while j < len(data):
            c = data[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        return data[i : j + 1]
    return None


def parse_full_tags(data):
    i = data.find("const FULL_TAGS = [")
    if i < 0:
        raise SystemExit("超市 HTML 里找不到 const FULL_TAGS")
    start = i + len("const FULL_TAGS = [")
    j = data.find("];", start)
    raw = data[start:j]
    return re.findall(
        r'\[\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*([0-9-]+)\s*,\s*([0-9-]+)\s*\]', raw
    )


def parse_curated(data):
    """CURATED: 分类 -> [英文标签...]"""
    obj = extract_obj(data, "CURATED")
    if not obj:
        return {}
    cats = {}
    for m in re.finditer(r'"([^"]+)":\s*\[(.*?)\]', obj, re.S):
        cat, body = m.group(1), m.group(2)
        tags = re.findall(r'"([^"]+)"', body)
        cats[cat] = tags
    return cats


def parse_curated_zh(data):
    """CURATED_ZH: 英文(空格下划线归一) -> 中文"""
    obj = extract_obj(data, "CURATED_ZH")
    if not obj:
        return {}
    zh = {}
    for k, v in re.findall(r"'([^']+)'\s*:\s*'([^']*)'", obj):
        zh[normalize(k)] = v
    return zh


def normalize(s):
    return s.strip().lower().replace("_", " ")


def cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def build_db(full_tags):
    seen = set()
    rows = []
    for en, zh, t, cnt in full_tags:
        if t not in ("0", "3", "4"):
            continue
        if not cjk(zh) or zh == en or not en or not zh:
            continue
        if en in seen:
            continue
        seen.add(en)
        rows.append([zh, en])
    return rows


# 补充词（精选库用）：中文 -> 英文。写实/摄影 + 补充 NSFW（成人自用口径）
SUPPLEMENTS = [
    # 写实 / 摄影（自然语言流）
    ["逆光", "backlight"],
    ["逆光剪影", "backlit silhouette"],
    ["霓虹灯", "neon light"],
    ["硬光", "hard light"],
    ["自然光", "natural light"],
    ["暖色调", "warm color tone"],
    ["冷色调", "cool color tone"],
    ["背景虚化", "bokeh"],
    ["湿身", "wet body"],
    ["汗湿皮肤", "sweaty skin"],
    ["潮红皮肤", "flushed skin"],
    ["泪光", "teary eyes"],
    ["素颜", "bare face"],
    ["妆容精致", "detailed makeup"],
    # 补充 NSFW（成人自用口径）
    ["舔阴", "cunnilingus"],
    ["足交", "footjob"],
    ["颜射", "facial"],
    ["深喉", "deepthroat"],
    ["肛交", "anal sex"],
    ["3P", "threesome"],
    ["乳交", "paizuri"],
    ["精液", "white cum"],
    ["后宫", "harem"],
    ["露出", "exhibitionism"],
    ["淫乱表情", "lewd expression"],
    # 常用主体同义词（用户口语 → 标准标签）
    ["少女", "1girl"],
    ["女子", "1girl"],
    ["女人", "1girl"],
    ["女孩", "1girl"],
    ["少年", "1boy"],
    ["男子", "1boy"],
    ["男人", "1boy"],
    ["男孩", "1boy"],
    ["性爱", "sex"],
    ["做爱", "sex"],
    ["亲吻", "kissing"],
    ["裸", "nude"],
]


def build_curated(full_tags, curated, curated_zh):
    full = {}
    for en, zh, t, cnt in full_tags:
        if t != "0" and not zh:
            continue
        full.setdefault(normalize(en), zh)
    seen_en = set()
    rows = []
    for cat, tags in curated.items():
        if cat == "负面词":
            continue
        for en in tags:
            if not en or en in seen_en:
                continue
            zh = curated_zh.get(normalize(en)) or full.get(normalize(en)) or ""
            if zh and cjk(zh):
                seen_en.add(en)
                rows.append([zh, en])
    seen_pair = set()
    for zh, en in SUPPLEMENTS:
        key = (zh, en)
        if key in seen_pair:
            continue
        seen_pair.add(key)
        rows.append([zh, en])
    rows.sort(key=lambda r: r[0])
    return rows


def js_rows(rows):
    # var (not const): 顶层 var 会挂到 window 上，脚本加载后 window.PROMPT_DB 可读
    return "var PROMPT_DB=[" + ",".join(
        "[" + json.dumps(zh, ensure_ascii=False) + "," + json.dumps(en, ensure_ascii=False) + "]"
        for zh, en in rows
    ) + "];"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("supermarket", nargs="?", default=r"E:\AI\ai-image\AI 绘画提示词超市.html")
    ap.add_argument("--db-out", default="prompt-db.js")
    ap.add_argument("--curated-out", default="curated-lib.js")
    a = ap.parse_args()

    data = read_file(a.supermarket)
    full = parse_full_tags(data)
    curated = parse_curated(data)
    curated_zh = parse_curated_zh(data)
    print("FULL_TAGS:", len(full))

    db = build_db(full)
    with open(a.db_out, "w", encoding="utf-8", newline="\n") as f:
        f.write(js_rows(db))
    print("prompt-db.js: %d 条 -> %.1f MB" % (len(db), os.path.getsize(a.db_out) / 1e6))

    curated_rows = build_curated(full, curated, curated_zh)
    js = "const CURATED_LIB=[" + ",".join(
        "[" + json.dumps(zh, ensure_ascii=False) + "," + json.dumps(en, ensure_ascii=False) + "]"
        for zh, en in curated_rows
    ) + "];"
    with open(a.curated_out, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    print("curated-lib.js: %d 条 -> %.1f KB" % (len(curated_rows), os.path.getsize(a.curated_out) / 1024))
    print("精选库样例:")
    for zh, en in curated_rows[:8]:
        print("  ", zh, "->", en)


if __name__ == "__main__":
    main()
