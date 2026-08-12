#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地 CORS 代理 — 让 file:// 页面（AI 提示词工坊）能访问 opencode API
转发到 https://opencode.ai/zen/go/v1，自动加 CORS 头 + 处理 OPTIONS 预检。

用法: python opencode_proxy.py [端口=7898]
"""
import json, os, subprocess, sys, http.server

# ================= 在这里填你的配置 =================
# 1) API Key：把下面的空引号换成你的 key，例如 API_KEY = "sk-l75..."
#    留空 "" 则自动读取：环境变量 OPENCODE_API_KEY → opencode 认证文件 auth.json
API_KEY = ""

# 2) 可选：模型名 / 网关地址（一般不用改）
MODEL = "deepseek-v4-flash"
UPSTREAM = "https://opencode.ai/zen/go/v1"
# ===================================================

AUTH = os.path.expanduser("~/.local/share/opencode/auth.json")
MODEL = os.environ.get("OPENCODE_MODEL", MODEL)
UPSTREAM = os.environ.get("OPENCODE_BASE_URL", UPSTREAM)


def _api_key():
    k = (API_KEY or "").strip()
    if k:
        return k
    k = os.environ.get("OPENCODE_API_KEY", "").strip()
    if k:
        return k
    try:
        return json.load(open(AUTH, encoding="utf-8"))["opencode"]["key"]
    except Exception:
        return ""


API_KEY = _api_key()


class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.rstrip("/").endswith("/models"):
            data = json.dumps({"data": [{"id": MODEL, "object": "model"}]}).encode()
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_response(404)
        self._cors()
        self.end_headers()

    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(ln)
        path = self.path[3:] if self.path.startswith("/v1") else self.path   # 去掉 /v1 前缀（UPSTREAM 已含）
        url = UPSTREAM + path
        try:
            # 用 curl 转发（Python urllib 的 TLS 握手在本网络会被掐，curl 稳定）
            p = subprocess.run(
                ["curl", "-s", "-w", "\n%{http_code}", "-m", "180", "-X", "POST", url,
                 "-H", "Authorization: Bearer " + API_KEY,
                 "-H", "Content-Type: application/json",
                 "--data-binary", "@-"],
                input=body, capture_output=True, timeout=190)
            out = p.stdout
            code = 502
            resp = out
            if b"\n" in out:
                head, _, tail = out.rpartition(b"\n")
                try:
                    code = int(tail.strip())
                except Exception:
                    code = 502
                resp = head
            self.send_response(code)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp)
        except Exception as e:
            self.send_response(502)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": {"message": str(e)}}).encode())

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7898
    if not API_KEY:
        print("⚠️ 未检测到 API Key —— 请在 opencode_proxy.py 顶部 API_KEY = \"\" 填入你的 key（或设置环境变量 OPENCODE_API_KEY）")
    print(f"opencode CORS proxy on http://127.0.0.1:{port}/v1  (model={MODEL}, key={API_KEY[:8]}...)")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
