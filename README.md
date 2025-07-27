# Weather Agent 示例项目（基于函数调用）

本项目展示了一个使用函数调用（Function Calling）能力的轻量智能体，用于完成如下任务：

> 查询指定城市（如深圳）的天气，并根据天气信息，自动给出是否需要带伞的建议。


## 🧠 功能亮点

- 使用大语言模型Qwen-Plus分析用户意图；
- 识别是否需要调用外部函数获取数据；
- 通过 `get_weather(city)` 函数模拟外部天气 API；
- 最终由模型基于函数返回结果，自动给出建议。


## ⏳ 环境依赖

1、安装以下依赖：

- Python ≥ 3.8
- `openai` Python SDK（支持 DashScope 接入）

2、安装依赖：

```bash
pip install openai
```


## 🚀 如何运行

1、设置 DashScope API Key（以环境变量方式更安全）：

```bash
export DASHSCOPE_API_KEY=sk-xxx   # 这里替换为真实 API Key
```

2、执行命令：

```bash
python test.py
```

然后根据提示输入：

```
查找深圳的天气，然后用一句话告诉我出门要不要带伞
```

模型将自动调用函数获取天气，并综合判断是否建议带伞。


## 🫴借助GPT部分

在调试中发现基于原有的get_weather无法识别中文的城市，因此构建了city_map如下，以识别中英文的城市输入：
```bash
city_map = {
        "beijing": "beijing",
        "北京": "beijing",
        "shenzhen": "shenzhen",
        "深圳": "shenzhen"
    }
```
