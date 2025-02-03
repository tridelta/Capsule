import random
from http import HTTPStatus
from dashscope import Generation
from .utils import get_secret


def ask_qwen(prompt: str, model_name="qwen-turbo"):
    # 确保API Key已经设置
    api_key = get_secret("llm.qwen")
    if api_key is None:
        raise ValueError("请确保 `SECRET:llm.qwen` 已设置")

    # 准备消息列表
    messages = [{'role': 'user', 'content': prompt}]

    # 创建并初始化请求对象
    response = Generation.call(
        model_name,
        messages=messages,
        # 设置随机种子,可选,默认为1234(这里假设sdk支持随机种子设置)
        seed=random.randint(1, 10000),
        # 设置结果格式为message
        result_format='message',
        api_key=api_key
    )

    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0]['message']['content']
    else:
        error_message = f"请求ID: {response.request_id}, 状态码: {response.status_code}, 错误代码: {response.code}, 错误信息: {response.message}"
        raise Exception(error_message)


# test
if __name__ == "__main__":
    try:
        question = "如何制作一杯卡布奇诺咖啡?"
        answer = ask_qwen(question)
        print(f"助手的回答:{answer}")
    except Exception as e:
        print(f"调用API时出错:{e}")