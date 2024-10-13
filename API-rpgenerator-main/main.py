from fastapi import FastAPI
from pydantic import BaseModel
import requests
from openai import OpenAI
# Para gerar histórias, você precisará de uma chave da OpenAI

app = FastAPI()

client = OpenAI(
  organization="org-m1a5hGjn7D2AT4XAoFnNCdXL",
  project="proj_DBKA77qdzOvNDBAQhumQ7OO2",
  #colocar a chave da api
  api_key="sk-6pPYIULZuX9--OSYrVxoN8oGLXYM8OPZgWR-_ksE4oT3BlbkFJfZ7nyTCYn9ENCIHgJUCqvS14-s6NDZ0_Ermv_2djIA"
)


# Modelo para validação dos dados de entrada
class PromptRequest(BaseModel):
    prompt: str

# Chave da API da Giphy
#giphy_api_key = "YOUR_GIPHY_API_KEY"
giphy_api_key = "DmPomXT2VYbsMDwPULwsoSnxdSdRLU47"
# Rota para melhorar o prompt
@app.post("/melhorar_prompt")
async def melhorar_prompt(prompt: PromptRequest):
    # Aqui você implementaria a lógica para melhorar o prompt
    # Por exemplo, usando técnicas de NLP ou um modelo de linguagem
    prompt_melhorado = f"Prompt melhorado: {prompt.prompt.upper()}"  # Exemplo simples
    return {"prompt_melhorado": prompt_melhorado}

# Rota para buscar imagens
@app.post("/buscar_imagens")
async def buscar_imagens(prompt: PromptRequest):
    url = f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q={prompt.prompt}&limit=10"
    response = requests.get(url)
    data = response.json()
    imagens = [item['images']['original']['url'] for item in data['data']]
    return {"imagens": imagens}

# Rota para gerar histórias
@app.post("/gerar_historia")
async def gerar_historia(prompt: PromptRequest):
    

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a rpg master making a new history."},
            {
                "role": "user",
                "content": f"Write a story based on: {prompt.prompt}"
            }
        ]
    )

    historia = completion.choices[0].message
    return {"historia": historia}