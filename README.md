# AI 提示词工坊（AI Prompt Studio）

![](https://img.shields.io/badge/version-v1.1.0-blue)

**中文简体** | [**English**](./docs/en/README.md)

把中文需求（自由描述，NSFW 也直接写）自动转成英文提示词，单文件、零依赖，浏览器打开即用：

- **🎨 SDXL 生图**：Stable Diffusion 直白英文提示词（标签流 / 自然语言流）+ 负面提示词
- **🎬 H3 视频**：MiniMax H3 结构化英文提示词（T2VA / I2VA / FL2VA / L2VA / Ref2VA × 文戏 / 武戏 / 九宫格）

## 功能

- **标签流**（NoobAI / Pony / Manhwa）：Danbooru 标签 + `masterpiece, best quality, newest, absurdres` 质量前缀
- **自然语言流**（RealVis / Juggernaut）：`RAW photo` 开头的自然语言提示词 + 相机/镜头/光线词
- **提示词库参考**：精选库（内嵌 347 条常用标签，默认）/ 全量库（16.7 万条，首次联网加载 `prompt-db.js`，仅浏览器内存检索，不占模型上下文）
- **负面提示词自动生成**：本地与在线模型都实时生成匹配负面，失败回退通用默认
- **H3 视频提示词**：生成模式（T2VA 纯文字 / I2VA 首帧 / FL2VA 首尾帧 / L2VA 尾帧 / Ref2VA 参考）+ 内容风格（文戏 / 武戏 / 九宫格），输出官方结构化格式（base 三字段 / Ref2VA 六段），内置 H3 NSFW 实测经验（年龄双写、亚洲脸特征、声音少堆叠、出画收束等）
- **NSFW 直白度滑杆**（保守 / 标准 / 直白 / 高度直白）
- **内置直白词典**作为知识库：命中词强制用标准英文词
- **多后端**：本地 llama / OpenAI / DeepSeek / 自定义（OpenAI 兼容），在线源附官网地址与风险提示
- **自适应**：手机 / 桌面自动缩放

## 快速开始

1. 下载 `index.html`（要用全量库再下载 `prompt-db.js` 放同目录），双击用浏览器打开
2. 选「模型源」→ 填 Base URL / 模型 / Key → 输入中文需求 → 点「转换 →」
3. 顶部页签切换「🎨 SDXL 生图」或「🎬 H3 视频」
4. 生成结果复制到 SD WebUI / ComfyUI / MiniMax H3 工作流

## 后端说明

| 后端 | Base URL | 说明 |
|------|----------|------|
| **本地 llama** | `http://127.0.0.1:4001/v1` | 需先本机启动 OpenAI 兼容的 llama-server（如 Qwen3-4B） |
| **OpenAI** | 官方 API | 申请 Key：https://platform.openai.com |
| **DeepSeek** | 官方 API | 申请 Key：https://platform.deepseek.com |
| **自定义** | 任意 OpenAI 兼容端点 | 如 opencode 网关（见下） |

> ⚠️ 在线源会把你的提示词（含 NSFW / 隐私内容）发送到第三方服务，可能被记录或用于内容审核，请自行承担风险。API Key 仅保存在本机浏览器（localStorage）。
>
> 上下文建议：SDXL 生图 ≥8192，H3 视频 ≥8192（负面提示词也由模型生成）。全量库 16.7 万条仅在浏览器内存检索，不占模型上下文。

### 接入 opencode API（需本地代理）

opencode 网关 **`https://opencode.ai/zen/go/v1`** 不返回 CORS 头，浏览器页面无法直连，需本地代理转发：

```bash
# 1. 打开 opencode_proxy.py，把顶部 API_KEY = "" 换成你的 key
#    （留空则自动读取 opencode 认证文件 ~/.local/share/opencode/auth.json 或环境变量 OPENCODE_API_KEY）
# 2. 启动代理（默认端口 7898）
python opencode_proxy.py
```

然后在「自定义」里填：Base URL `http://127.0.0.1:7898/v1`、模型 `deepseek-v4-flash`、Key 任意。

> 推理模型（Qwen3-4B / deepseek-v4-flash 等）会先"思考"，页面已自动禁用思考并调大 token 预算，直接出结果。

## 提示词库参考

- **精选库（默认）**：内嵌 347 条常用标签（质量词 / 发色 / 表情 / 身材 / 服装 / 姿势 / 场景 / 画风 / NSFW / 写实词汇），离线可用。
- **全量库**：16.7 万条（通用描述 + 作品系列 + 角色名，取自「AI 绘画提示词超市」全量库的类型 0/3/4）。首次选中联网加载 `prompt-db.js`（约 7.6MB），在浏览器内存检索，每轮只把命中 ≤80 条发送给模型，不占模型上下文。

## H3 视频提示词

- **生成模式**（输入类型）：T2VA 纯文字（试水 / 氛围片）、I2VA 首帧起步、FL2VA 首尾帧插值、L2VA 尾帧反推定格、Ref2VA 角色一致性 + 音色 + 对嘴型。
- **内容风格**：文戏（关系转折 / 对白）、武戏（高密度攻防，内置节奏预算）、九宫格（3×3 故事板，先生成出图提示词，出图后再生成视频提示词）。
- 输出官方结构化格式：base 模式三字段（`integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`），Ref2VA 六段，含对齐指令行；参考图用文字描述，无需上传图片。

## 负面提示词

- 本地与在线模型都实时生成匹配负面提示词；生成失败或为空时回退通用默认（`easynegative, bad-hands, ...`）。

## 在线使用

本项目已托管到 GitHub Pages：**https://bfrkqsb7.github.io/sd-prompt-converter/**

- **OpenAI / DeepSeek**：在线版可直接用（官方 API 带 CORS 头）
- **本地 llama / opencode / 全量库**：在线版无法直连（CORS / 浏览器私有网络限制）——下载 `index.html` + `prompt-db.js`（+ `opencode_proxy.py`）本地打开，功能完整

## License

MIT
