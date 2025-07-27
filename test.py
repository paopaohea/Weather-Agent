import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 用的是qwen-plus
)

functions = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "要查询天气的城市，例如：'Shenzhen'"
                }
            },
            "required": ["city"]
        }
    }
]

def get_weather(city: str) -> str:
    # 增加一个城市名称的映射表
    city_map = {
        "beijing": "beijing",
        "北京": "beijing",
        "shenzhen": "shenzhen",
        "深圳": "shenzhen"
    }

    weather_data = {
        "beijing": {
            "location": "Beijing",
            "temperature": {
                "current": 32,
                "low": 26,
                "high": 35
            },
            "rain_probability": 10,   # 百分比
            "humidity": 40  # 百分比
        },
        "shenzhen": {
            "location": "Shenzhen",
            "temperature": {
                "current": 28,
                "low": 24,
                "high": 31
            },
            "rain_probability": 90,   # 百分比
            "humidity": 85     # 百分比
        }
    }

    #为了确保用户输入为中文时，也可以响应
    city_key = city_map.get(city.lower())

    if city_key and city_key in weather_data:
        return json.dumps(weather_data[city_key], ensure_ascii=False)
    return json.dumps({"error": "Weather Unavailable"}, ensure_ascii=False)

def agent_task():
    user_question = input("您好，请问需要什么帮助？\n>>>")

    messages = [{"role": "user", "content": user_question}]
    tools = [{"type": "function", "function": f} for f in functions]

    # 第一步：让模型理解任务并决定是否调用工具
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    # 调试
    # print("Raw response:", response)

    response_message = response.choices[0].message

    if response.choices[0].finish_reason == "tool_calls":
        # 将回复（包含工具调用请求）添加到消息历史中
        messages.append(response_message)
        
        # 循环处理所有工具调用，但此任务中只有一个
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # 执行本地函数
            if function_name == "get_weather":
                function_response = get_weather(city=arguments.get("city"))
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

        # 第二步：将函数结果继续交给模型总结
        followup = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
        )
        print("模型建议：", followup.choices[0].message.content)
    else:
        # 如果模型没有调用工具，直接打印其回答
        print("模型没有调用任何函数，直接回复如下：",response_message.content)

# --主程序--
if __name__ == "__main__":
    agent_task()