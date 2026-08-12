# SD 提示词转换器（Prompt Converter）

![](https://img.shields.io/badge/version-v1.0.0-blue)

**中文简体** | [**English**](./docs/en/README.md)

把中文需求（自由描述画面，NSFW 也直接写）自动转成 **Stable Diffusion 直白英文提示词**。单文件、零依赖，浏览器打开即用。

## 功能

- **标签流**（NoobAI / Pony / Manhwa）：输出 Danbooru 标签 + `masterpiece, best quality, newest, absurdres` 质量前缀
- **自然语言流**（RealVis / Juggernaut）：输出 `RAW photo` 开头的自然语言提示词 + 相机/镜头/光线词
- **NSFW 直白度滑杆**（保守 / 标准 / 直白 / 高度直白）：控制措辞直白程度
- **内置直白词典**作为知识库：命中词强制用标准英文词，避免委婉语/自造近义词
- **负面提示词自动生成**：本地模型输出通用默认负面；在线模型实时生成匹配负面
- **多后端**：本地 llama / OpenAI / DeepSeek / 自定义（OpenAI 兼容）

## 快速开始

1. 下载 `index.html`，双击用浏览器打开（无需安装）
2. 选「模型源」→ 填 Base URL / 模型 / Key → 输入中文需求 → 点「转换 →」
3. 生成结果复制到 SD WebUI / ComfyUI 使用

## 后端说明

| 后端 | 配置 | 说明 |
|------|------|------|
| **本地 llama** | Base URL `http://127.0.0.1:4001/v1` | 需先本机启动 OpenAI 兼容的 llama-server（如 Qwen3-4B） |
| **OpenAI** | 官方 API | 填 Key 即用 |
| **DeepSeek** | 官方 API | 填 Key 即用 |
| **自定义** | 任意 OpenAI 兼容端点 | 如 opencode 网关（见下） |

### 接入 opencode API（需本地代理）

opencode 网关 **`https://opencode.ai/zen/go/v1`** 不返回 CORS 头，浏览器页面无法直连，需本地代理转发：

```bash
# 方式一：设置环境变量（或用 opencode 默认认证文件，代理会自动读取）
set OPENCODE_API_KEY=sk-...
# 启动代理（默认端口 7898）
python opencode_proxy.py
```

然后在「自定义」里填：Base URL `http://127.0.0.1:7898/v1`、模型 `deepseek-v4-flash`、Key 任意。

> 推理模型（Qwen3-4B / deepseek-v4-flash 等）会先"思考"，页面已自动禁用思考并调大 token 预算，直接出结果。

## 负面提示词

- **本地模型**（负担重）：自动填通用默认负面（`easynegative, bad-hands, ...`）
- **在线模型**：根据正向提示词实时生成匹配的负面提示词

## 部署到 GitHub Pages

把 `index.html` 放仓库根目录即可（Pages 自动托管为首页）。注意：

- **Pages 上在线源**：OpenAI / DeepSeek 可直接用（带 CORS 头）
- **Pages 上 opencode**：因 CORS + 浏览器私有网络限制，**建议下载本地使用**（`index.html` + `opencode_proxy.py`），不要在托管页直接连 opencode

## License

MIT
