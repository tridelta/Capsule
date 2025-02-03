import os

_SECRETS = {
    "llm": {
        "qwen": os.getenv("SECRET_LLM_QWEN")
    }
}

def get_secret(s: str):
    services = s.split(".")
    
    target = _SECRETS
    while services:
        service = services.pop(0)
        target = target.get(service)

    return target
    