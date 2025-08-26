# WebSearchAPI

一个基于 FastAPI 的 Web 搜索 API 服务，集成了讯飞星火和百度 AI 搜索功能。

## 功能特性

- 🔍 **讯飞星火搜索**：集成讯飞星火聚合搜索工具
- 🤖 **百度 AI 搜索**：支持百度千帆 AI 搜索服务
- ⚡ **异步处理**：基于 FastAPI 的高性能异步 API
- 📝 **参数化配置**：灵活的搜索参数配置
- 🛡️ **错误处理**：完善的异常处理和错误响应

## 项目结构

```
WebSearchAPI/
├── main.py                    # 主应用入口
├── router/
│   └── xfyun_websearch.py     # 搜索 API 路由
├── test_main.http             # API 测试文件
└── README.md                  # 项目说明文档
```

## 环境要求

- Python 3.8+
- FastAPI
- httpx
- pydantic

## 安装依赖

```bash
pip install fastapi uvicorn httpx pydantic
```

## 环境变量配置

在使用百度 AI 搜索功能前，需要设置环境变量：

```bash
# Windows
set BAIDU_API_KEY=your_baidu_api_key

# Linux/macOS
export BAIDU_API_KEY=your_baidu_api_key
```

## 启动服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后，可以通过以下地址访问：
- API 文档：http://localhost:8000/docs
- 交互式文档：http://localhost:8000/redoc

## API 接口

### 1. 讯飞星火搜索

**接口地址：** `POST /xfyun/websearch`

**参数说明：**
- `search_keyword` (string, required): 搜索关键词
- `limit` (integer, optional): 返回网页数量，默认为 3

**请求示例：**
```bash
curl -X POST "http://localhost:8000/xfyun/websearch?search_keyword=人工智能&limit=5" \
     -H "Content-Type: application/json"
```

### 2. 百度 AI 搜索

**接口地址：** `POST /xfyun/baidu-search`

**参数说明：**
- `content` (string, required): 搜索内容，用户输入的查询关键词或问题
- `search_source` (string, optional): 搜索源，默认为 "baidu_search_v2"
- `resource_type_filter` (array, optional): 资源类型过滤器，默认为网页搜索前10条
- `search_filter` (object, optional): 搜索过滤器，用于精确控制搜索条件
- `search_recency_filter` (string, optional): 时间过滤器，默认为 "year"

**请求示例：**
```bash
curl -X POST "http://localhost:8000/xfyun/baidu-search" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "最新的人工智能发展趋势",
       "search_recency_filter": "month"
     }'
```

### 3. 基础接口

- `GET /`: 返回欢迎消息
- `GET /hello/{name}`: 个性化问候

## 响应格式

### 成功响应
所有 API 接口在成功时返回 JSON 格式的搜索结果。

### 错误响应
```json
{
  "detail": "错误描述信息"
}
```

常见错误码：
- `400`: 请求参数错误
- `500`: 服务器内部错误
- `502`: 外部 API 调用失败

## 开发说明

### 讯飞星火搜索配置

讯飞星火搜索需要有效的会话信息，包括：
- JSESSIONID
- account_id
- ssoSessionId

这些信息需要从浏览器的开发者工具中获取，并更新到代码中的 Cookie 字段。

### 百度 AI 搜索配置

百度 AI 搜索使用千帆平台的 API，需要：
1. 在百度智能云注册账号
2. 开通千帆大模型平台服务
3. 获取 API Key
4. 设置环境变量 `BAIDU_API_KEY`

## 注意事项

1. **认证信息更新**：讯飞星火的认证信息有时效性，需要定期更新
2. **API 限制**：注意各平台的 API 调用频率限制
3. **网络超时**：所有外部 API 调用设置了 30 秒超时
4. **错误处理**：建议在客户端实现重试机制

