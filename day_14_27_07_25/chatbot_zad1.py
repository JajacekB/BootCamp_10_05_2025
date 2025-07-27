from openai import OpenAI
import os

# pip install openai

class ChatBot:
    def __init__(self, model="gpt-3.5-turbo"):
    # def __init__(self, model="gpt-4-0613"):
    # def __init__(self, model="gpt-4.1"):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.message = []
        self.model = model

    def add_message(self, role, content):
        if role in ["user", "assistant"]:
            self.message.append(
                {"role": role, "content": content}
            )
        else:
            raise ValueError("Role must be 'user' or 'assistant'!")

    def get_models(self):
        print([m.id for m in self.client.models.list().data])

    def get_response(self, user_message):
        self.add_message("user", user_message)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.message
        )
        # print(response)

        model_message = response.choices[0].message.content
        self.add_message("assistant", model_message)
        return model_message


bot = ChatBot()

if __name__ == '__main__':
    print("Starting")

    

    # bot.get_models()
    print(bot.get_response("Opisz Comarch"))
    print(bot.get_response("Kto jest jego włascicielem"))
