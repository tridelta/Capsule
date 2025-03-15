# from .qwen import ask_qwen
from ...ConfigService import get_secret
from .openai_api import ask_custom, custom_ask

model_api_map = {
    # 'qwen': ask_qwen
    "lwai": custom_ask("https://llm.cxzlw.top", get_secret("llm.lwai"), "gpt-4o")
}

def ask_llm(model, prompt, **kwargs):
    ask_xxx = model_api_map.get(model)
    if ask_xxx is None:
        raise ValueError(f"Model {model} not found.")
    
    return ask_xxx(prompt, **kwargs)


if __name__ == "__main__":
    print(get_secret("llm.lwai"))