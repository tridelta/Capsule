from .qwen import ask_qwen

model_api_map = {
    'qwen': ask_qwen
}

def ask_llm(model, prompt, **kwargs):
    ask_xxx = model_api_map.get(model)
    if ask_xxx is None:
        raise ValueError(f"Model {model} not found.")
    
    return ask_xxx(prompt, **kwargs)

