from transformers import pipeline

chatbot = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")
response = chatbot("Cześć, jak mogę Ci pomóc?")
print(response[0]['generated_text'])