# pip install transformers torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)

print("🤖 GPT - Mini czat lokalny. Wpisz 'exit', aby zakończyć.")
chat_history_ids = None

while True:
    user_input = input("\n👤 Ty: ")
    if user_input.lower() in ["exit", "quit", "wyjście"]:
        print("Zakończono rozmowę.")
        break

    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = torch.cat([chat_history_ids, new_input_ids],
                              dim=-1) if chat_history_ids is not None else new_input_ids

    attention_mask = torch.ones(bot_input_ids.shape, dtype=torch.long)

    chat_history_ids = model.generate(
        bot_input_ids,
        attention_mask=attention_mask,
        max_length=500,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    print(f"🤖 GPT: {response}")