from transformers import AutoModelForCausalLM, AutoTokenizer


class LLM:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

        self.model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen3-0.6B")


    def genrate_answer(self, prompt: str)-> str:
        inputs = self.tokenizer(prompt,return_tensors="pt")
        outputs = self.model.generate(**inputs,max_new_tokens=256,do_sample=False,
                                      pad_token_id=self.tokenizer.eos_token_id)
        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        answer = self.tokenizer.decode(generated_ids,skip_special_tokens=True)
        return answer
