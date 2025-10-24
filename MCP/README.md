### 启动命令
```
mcp dev server.py
```
### 配置文件 
#### stdio
```
    "getWeather_server": {
      "command": "D:/Python3.10.11/Scripts/uv.exe",
      "args": [ 
        "--directory",  
        "D:/AIAgent/PyMcp",
        "run","--with","mcp","mcp","run","main.py"
      ],
     
      "autoApprove": [
        "get_weather"
      ]
    }
```
#### sse 官方已弃用
```
    "getWeather_server-mcp": {
      "url": "http://10.10.1.236:8000/sse",
      "disabled": false,
      "autoApprove": []
    }
```
#### http
```
 uv run httpServer.py --api_key=5571195b5a51823c4719a4bbf9de836f

 {
    "getWeather-mcp-server": {
        "transport": "streamable_http",
        "url": "http://927ebba.r16.vip.cpolar.cn/mcp/",
        "timeout": 6000
    }
}
```
### 发布到服务器 使用http
