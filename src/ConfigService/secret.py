"""
ConfigService/secret.py
=======================

This module provides a unified way to access/manage API secrets and other credentials.
"""

import os
from dotenv import load_dotenv

load_dotenv('./ConfigService/secrets.env')

_SECRETS = {
    "llm": {
        # "qwen": os.getenv("SECRET_LLM_QWEN"),
        "lwai": os.getenv("SECRET_LLM_CXZLW_COM"),
    }
}

def get_secret(s: str):
    services = s.split(".")
    
    target = _SECRETS
    while services:
        service = services.pop(0)
        target = target.get(service)

    return target
    