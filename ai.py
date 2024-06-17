import replicate


def response(prompt, max_new_tokens: int = 250) -> str:
    concat: str = ''
    for event in replicate.stream(
            "meta/llama-2-70b-chat",
            input={
                "prompt": prompt,
                "max_new_tokens": max_new_tokens
            },
    ):
        concat += str(event)
    return concat
