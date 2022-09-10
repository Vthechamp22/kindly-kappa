import os

import requests


def evaluate(code: str) -> str:
    """Evaluate code thanks to the snekbox API.

    Args:
        code: The code to evaluate.
    """
    eval_url = os.environ.get("EVAL_URL", default="http://localhost:8060/eval")

    response = requests.post(eval_url, json={"input": code})
    return response.json()["stdout"]
