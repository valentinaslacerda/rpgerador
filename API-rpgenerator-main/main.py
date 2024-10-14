from fastapi import FastAPI
from pydantic import BaseModel
import requests
from openai import OpenAI
import google.generativeai as genai
from google.api_core import retry

# Para gerar histórias, você precisará de uma chave da OpenAI

#pegar a key da api da google pelo .env
from dotenv import load_dotenv
import os

load_dotenv()

api_key_gemini = os.getenv("API_KEY_GEMINI")

app = FastAPI()

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
    url = f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q={prompt.prompt}&limit=10"
    response = requests.get(url)
    data = response.json()
    imagens = [item['images']['original']['url'] for item in data['data']]
    return {"imagens": imagens}

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