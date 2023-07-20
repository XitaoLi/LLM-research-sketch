import os
import openai
from tqdm import tqdm
import json
import time

class Client:
    def __init__(self,model) -> None:
        """
        Models: gpt-3.5-turbo, gpt-4, gpt-4-32k
        """
        openai.api_type = "azure"
        openai.api_base = os.getevn
        openai.api_version = "2023-05-15"
        openai.api_key = os.getevn #os.getevn
        self.model = model
        self.restore_path = "restore_from_error.json"

    def get_response_chat_row(self,prompt,temperature,n,verbose=True):
        """"
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure Cognitive Services support this too?"}
            ]
        """
        max_attempts = 3
        success_flag = False
        for epoch in range(max_attempts):
            try:
                response = openai.ChatCompletion.create(
                    engine=self.model, # engine = "deployment_name".
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    n=n
                )
                success_flag = True
                break
            except openai.error.RateLimitError:
                print("RateLimit")
                time.sleep(60*(epoch + 1))
            except Exception as e:
                raise e

        time.sleep(12)
        if not success_flag:
            raise openai.error.RateLimitError
        elif verbose:
            return response
        elif n == 1:
            return response['choices'][0]['message']['content']
        else:
            return [response['choices'][i]['message']['content'] for i in range(n)]

    def get_response_chat(self,prompts,path,temperature,n,verbose=True):
        if os.path.exists(path):
            with open(path) as f:
                data_restore = json.load(f)
        else:
            data_restore = []

        start_idx = len(data_restore)
        for i,prompt in tqdm(enumerate(prompts[start_idx:]),total=len(prompts)-start_idx):
            try:
                response = self.get_response_chat_row(prompt,temperature,n,False)
                data_restore.append(response)
            except Exception as e:
                with open(path,"w") as f:
                    json.dump(data_restore,f,indent=4)
                print(response)
        with open(path,"w") as f:
            json.dump(data_restore,f,indent=4)    

def save_work(text,json_path):
    with open(json_path,"w") as f:
       json.dump(text,f,indent=4)        

if __name__ == "__main__":
    client = Client("gpt-4")
    print(client.get_response_chat_row("What's your name?",0,1))