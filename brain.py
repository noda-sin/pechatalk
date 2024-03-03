from openai import OpenAI


class Brain:
    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key=api_key)

    def reply(self, text: str) -> str:
        messages = [
            {"role": "user",
            "content": """
            あなたは娘の大好きなぬいぐるみ パグ蔵 になりきって会話をしてください。
            娘の名前は、ゆい です。娘のことは、ゆいちゃんと呼んでください。
            また、あなたは自身のことを 僕 と呼んでください。
            口調は、可愛く愛らしい印象を受ける口調でお願いします。
            全ての会話は、日本語で返答してください。
            返答はなるべく短い文章で返してください。
            """},
            {"role": "assistant", "content": "了解しました。"},
            {"role": "user", "content": text}
        ]
        return self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        ).choices[0].message.content
