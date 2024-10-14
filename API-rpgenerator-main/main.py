from fastapi import FastAPI
from pydantic import BaseModel
import requests
from openai import OpenAI
import google.generativeai as genai
from google.api_core import retry
from fastapi.middleware.cors import CORSMiddleware
import random

# Para gerar histórias, você precisará de uma chave da OpenAI

#pegar a key da api da google pelo .env
from dotenv import load_dotenv
import os

load_dotenv()

api_key_gemini = os.getenv("API_KEY_GEMINI")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# client = OpenAI(
#   organization="org-m1a5hGjn7D2AT4XAoFnNCdXL",
#   project="proj_DBKA77qdzOvNDBAQhumQ7OO2",
#   #colocar a chave da api
#   api_key="sk-6pPYIULZuX9--OSYrVxoN8oGLXYM8OPZgWR-_ksE4oT3BlbkFJfZ7nyTCYn9ENCIHgJUCqvS14-s6NDZ0_Ermv_2djIA"
# )

genai.configure(api_key=api_key_gemini)

# Modelo para validação dos dados de entrada
class PromptRequest(BaseModel):
    prompt: str

# Chave da API da Giphy
#giphy_api_key = "YOUR_GIPHY_API_KEY"
giphy_api_key = "DmPomXT2VYbsMDwPULwsoSnxdSdRLU47"

# promps base
base_prompts = {
    'persona': '''\
        Você é um premiado autor de ficção científica com uma propensão para histórias expansivas,
        intrincadamente tecidas. Seu objetivo final é escrever uma nova historia em um mundo de RPG.''',
    'guidelines': '''\
        Diretrizes de escrita

        Aprofunde-se. Perca-se no mundo que está construindo. Liberte descrições
        vívidas para pintar as cenas na mente do seu leitor. Desenvolva seus
        personagens — deixe suas motivações, medos e complexidades se desenrolarem naturalmente.
        Entrelace os fios do seu esboço, mas não se sinta limitado por ele. Permita
        que sua história o surpreenda enquanto você escreve. Use imagens ricas, detalhes sensoriais e
        linguagem evocativa para dar vida ao cenário, personagens e eventos.
        Apresente elementos sutilmente que podem florescer em subtramas complexas, relacionamentos
        ou detalhes de construção de mundo mais tarde na história. Mantenha as coisas intrigantes, mas não
        totalmente resolvidas. Evite encurralar a história muito cedo. Plante as sementes
        de subtramas ou possíveis mudanças de arco de personagem que podem ser expandidas mais tarde.

        Lembre-se, seu objetivo principal é escrever o máximo que puder. Se você terminar
        a história muito rápido, isso é ruim. Expanda, nunca resuma.
        ''',
}

function_prompts = {
    'premise_prompt': f'''\
    {base_prompts['persona']}
    Escreva uma premissa de uma única frase para uma história de RPG sobre {{detail}}.''',
    'outline_prompt': f'''\
    {base_prompts['persona']}

    Você tem uma premissa envolvente em mente:

    {{premise}}

    Escreva um esboço para o enredo da sua história.''',
    'starting_prompt': f'''\
    {base_prompts['persona']}

    Você tem uma premissa envolvente em mente:

    {{premise}}

    Sua imaginação criou um rico esboço narrativo:

    {{outline}}

    Primeiro, revise silenciosamente o esboço e a premissa. Pense em como começar a
    história.

    Comece a escrever o começo da história. Não se espera que você termine
    a história toda agora. Sua escrita deve ser detalhada o suficiente para que você esteja apenas
    arranhando a superfície do primeiro marcador do seu esboço. Tente escrever NO
    MÍNIMO 1000 PALAVRAS e NO MÁXIMO 2000 PALAVRAS.

    {base_prompts['guidelines']}''',
}

# Rota para melhorar o prompt
@app.post("/melhorar_prompt")
async def melhorar_prompt(prompt: PromptRequest):
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Create the model
    generation_config = {
        "temperature": 2,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    response = model.generate_content(prompt.prompt, generation_config=generation_config)

    # Aqui você implementaria a lógica para melhorar o prompt
    # Por exemplo, usando técnicas de NLP ou um modelo de linguagem
    prompt_melhorado = f"Prompt melhorado: {prompt.prompt.upper()}"  # Exemplo simples

    # model = genai.GenerativeModel("gemini-1.5-flash")
    # response = model.generate_content("Write a story about a magic backpack.")
    print(response.text)
    return {"prompt_melhorado": prompt_melhorado}

# Rota para buscar imagens
@app.post("/buscar_imagens")
async def buscar_imagens(prompt: PromptRequest):

    #usar o gemini para transformar o prompt em uma unicade de busca
    model = genai.GenerativeModel("gemini-1.5-flash")
    generation_config = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 64,
        "max_output_tokens": 10,
        "response_mime_type": "text/plain",
    }

    custom_prompt = f'''\
    propmpt: {prompt.prompt}

    lista: 
    noite
    dia
    floresta
    deserto
    cidade

    transforme o prompt em uma unica palavra da lista, responda com a palavra escolhida'''

    response = model.generate_content(custom_prompt, generation_config=generation_config).text

    noite_urls = [
        "https://reino-de-windblack.weebly.com/uploads/8/8/0/1/8801793/2088062.jpg?347",
        "https://nuckturp.com.br/wp-content/uploads/2022/09/Cenario-de-RPG-Nuckturp-Academia-de-Mestres-de-RPG.jpg",
        "https://preview.redd.it/8amf24k153371.jpg?width=640&crop=smart&auto=webp&s=d15461567bad9dd7c20ba9cb86400582dc1cf30b",
        "https://thumbs.dreamstime.com/b/mapa-de-rpg-fantasia-cima-para-baixo-e-rio-294882108.jpg"
    ]

    dia_urls = [
        "https://www.caixinhaquantica.com.br/wp-content/uploads/2022/04/CAPA-740x414.jpg",
        "https://universorpg.com/wp-content/uploads/2016/12/averum_cenario_de_campanha-e1481159899604.jpg",
        "https://movimentorpg.com.br/wp-content/uploads/2021/09/sistema-vs-cenari.jpg",
        "https://nuckturp.com.br/wp-content/uploads/2022/09/Cenario-de-RPG-Nuckturp-Academia-de-Mestres-de-RPG.jpg"
    ]

    floresta_urls = [
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg0pn1xh1USLJo684OIQlw0iVRDPTvxuEcQE79bhyW16R3Yx564jp84DWBXW4XdHGgK1DgsuaLilubkW3MgL2YESAshMsp9egTCTxqNME8Ce9hglxcF_1O8EKU80BcxFgBBFb9BWw3LlV7t/s1600/Imagem+16.jpg",
        "https://alaniarpg.weebly.com/uploads/1/7/5/4/17544523/5151719_orig.jpg",
        "https://alaniarpg.weebly.com/uploads/1/7/5/4/17544523/5146060_orig.jpg",
        "https://t3.ftcdn.net/jpg/07/79/45/10/360_F_779451098_RRBADWzwxiQPJMNv5Qxqk2wtARbio41v.jpg"
    ]

    deserto_urls = [
        "https://as2.ftcdn.net/v2/jpg/07/42/76/79/1000_F_742767963_Xz0Scki0oqj7izbsPH82AiARI0vMo2Qg.jpg",
        "https://as1.ftcdn.net/v2/jpg/08/23/15/18/1000_F_823151848_Ssmqlos87cUi4YVcFmdL9mfaR2n83zZm.jpg",
        "https://as2.ftcdn.net/v2/jpg/08/23/14/25/1000_F_823142562_0w3Uf9nzWUvUWTHebqfbSqRnDJnY0dhw.jpg",
        "https://as1.ftcdn.net/v2/jpg/08/47/73/94/1000_F_847739459_evBATeBaMZ1ZZXg3C1RK342vjBQ0xUs3.jpg"
    ]

    cidade_urls = [
        "https://pm1.aminoapps.com/7636/73c3df2475e5b59d705f7c4a65db7e45b65d850cr1-703-436v2_uhq.jpg",
        "https://overbr.com.br/wp-content/uploads/2013/02/droidscreens-epic-android.jpg",
        "https://miro.medium.com/v2/resize:fit:1024/0*38_yCPUTH0XpKTLY.jpg",
        "https://nuckturp.com.br/wp-content/uploads/2023/12/Cartografia-Mapa-Worldbuilding-Nuckturp-1-1024x574.png"
    ]

    response = response.strip()

    if response.lower() == "noite":
        escolhidos = random.sample(noite_urls, 1)
        print(escolhidos)
        return {"imagens": escolhidos}
    elif response.lower() == "dia":
        escolhidos = random.sample(dia_urls, 1)
        return {"imagens": escolhidos}
    elif response.lower() == "floresta":
        escolhidos = random.sample(floresta_urls, 1)
        return {"imagens": escolhidos}
    elif response.lower() == "deserto":
        escolhidos = random.sample(deserto_urls, 1)
        return {"imagens": escolhidos}
    elif response.lower() == "cidade":
        escolhidos = random.sample(cidade_urls, 1)
        return {"imagens": escolhidos}
    else:
        escolhidos = random.sample(cidade_urls, 1)
        return {"imagens": []}

# Rota para gerar histórias
@app.post("/gerar_historia")
async def gerar_historia(prompt: PromptRequest):
    persona = base_prompts['persona']
    guidelines = base_prompts['guidelines']
    premise_prompt = function_prompts['premise_prompt']
    outline_prompt = function_prompts['outline_prompt']
    starting_prompt = function_prompts['starting_prompt']

    generation_config = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel("gemini-1.5-flash")

    premise = model.generate_content(premise_prompt.format(detail=prompt.prompt), generation_config=generation_config, request_options={'retry':retry.Retry()}).text
    outline = model.generate_content(outline_prompt.format(premise=premise), generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    story_text = model.generate_content(starting_prompt.format(premise=premise, outline=outline), generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    context = {
        "premise": premise,
        "outline": outline,
        "story_text": story_text
    }

    return context

# Rota para gerar personagens
@app.post("/gerar_personagem")
async def gerar_personagem(prompt: PromptRequest):
    historia = await gerar_historia(prompt)
    historia_completa = historia
    historia = historia['story_text']

    generation_config = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel("gemini-1.5-flash")

    custom_prompt = f'''\
    {base_prompts['persona']}
    {historia}

    Escreva uma descrição detalhada de um personagem principal para a história acima.'''
    response = model.generate_content(custom_prompt, generation_config=generation_config).text

    context = {
        "personagem": response,
        "historia_completa": historia_completa
    }

    return context

#rota para gerar monstros
@app.post("/gerar_monstro")
async def gerar_monstro(prompt: PromptRequest):
    historia = await gerar_historia(prompt)
    historia_completa = historia
    historia = historia['story_text']

    generation_config = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel("gemini-1.5-flash")

    custom_prompt = f'''\
    {base_prompts['persona']}
    {historia}

    Escreva uma descrição detalhada de um monstro para a história acima.'''
    response = model.generate_content(custom_prompt, generation_config=generation_config).text

    context = {
        "monstro": response,
        "historia_completa": historia_completa
    }

    return context

#rota para gerar locais
@app.post("/gerar_local")
async def gerar_local(prompt: PromptRequest):
    historia = await gerar_historia(prompt)
    historia_completa = historia
    historia = historia['story_text']

    generation_config = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel("gemini-1.5-flash")

    custom_prompt = f'''\
    {base_prompts['persona']}
    {historia}

    Escreva uma descrição detalhada de um local para a história acima.'''

    response = model.generate_content(custom_prompt, generation_config=generation_config).text

    context = {
        "local": response,
        "historia_completa": historia_completa
    }

    return context

class PromptHistoria(BaseModel):
    premise: str
    outline: str
    story_text: str

#rota para gerar personagens de uma história
@app.post("/gerar_personagens_historia")
async def gerar_personagens_historia(request: PromptHistoria):
    historia = request.story_text

    generation_config = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel("gemini-1.5-flash")

    custom_prompt = f'''\
    {base_prompts['persona']}
    {historia}

    Escreva descrições detalhadas de um personagem para a história acima.'''

    response = model.generate_content(custom_prompt, generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    context = {
        "personagens": response,
    }

    return context

#rota teste para gerar história completa
@app.post("/gerar_historia_completa")
async def gerar_historia_completa(prompt: PromptRequest):
    persona = base_prompts['persona']
    guidelines = base_prompts['guidelines']
    premise_prompt = function_prompts['premise_prompt'].format(detail=prompt.prompt)
    outline_prompt = function_prompts['outline_prompt']
    starting_prompt = function_prompts['starting_prompt']

    generation_config = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 64,
        "max_output_tokens": 1512,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel("gemini-1.5-flash")

    premise = model.generate_content(premise_prompt.format(detail=prompt.prompt), generation_config=generation_config, request_options={'retry':retry.Retry()}).text
    outline = model.generate_content(outline_prompt.format(premise=premise), generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    story_text = model.generate_content(starting_prompt.format(premise=premise, outline=outline), generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    custom_prompt = f'''\
    {persona}
    {story_text}

    Escreva descrições detalhadas de 2 personagens para a história acima.'''

    personagens = model.generate_content(custom_prompt, generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    custom_prompt = f'''\
    {persona}
    {story_text}

    Escreva descrições detalhadas de 2 monstros para a história acima.'''

    monstros = model.generate_content(custom_prompt, generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    custom_prompt = f'''\
    {persona}
    {story_text}

    Escreva descrições detalhadas de um local para a história acima.'''

    locais = model.generate_content(custom_prompt, generation_config=generation_config, request_options={'retry':retry.Retry()}).text

    context = {
        "premise": premise,
        "outline": outline,
        "story_text": story_text,
        "personagens": personagens,
        "monstros": monstros,
        "locais": locais
    }

    return context