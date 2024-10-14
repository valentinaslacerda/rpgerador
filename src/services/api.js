const baseURL = 'http://127.0.0.1:8000';

/**
 * 
 * @param {string} propmt 
 * @returns 
 */
async function buscar_imagens(propmt) {

  try {
    const response = await fetch(`${baseURL}/buscar_imagens`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'allow-origin': '*',
      },
      body: JSON.stringify({
        prompt: propmt,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
}

/**
 * 
 * @param {string} propmt 
 * @returns 
 */
async function gerar_historia(propmt) {
  try {
    const response = await fetch(`${baseURL}/gerar_historia`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'allow-origin': '*',
        'acess-control-allow-origin': '*',
      },
      body: JSON.stringify({
        prompt: propmt,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
}

/**
 * 
 * @param {string} propmt 
 * @returns 
 */
async function gerar_personagem(propmt) {
  try {
    const response = await fetch(`${baseURL}/gerar_personagem`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: propmt,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
}

/**
 * @param {string} propmt
 * @return {Promise}
 */
async function gerar_monstro(propmt) {
  try {
    const response = await fetch(`${baseURL}/gerar_monstro`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: propmt,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
}

async function gerar_local(propmt) {
  try {
    const response = await fetch(`${baseURL}/gerar_local`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: propmt,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
}

/**
 * gerar personagem com base em uma historia
 * @param {{premise: str, outline: str, story_text: str}} historia
 * @return {Promise}
 */
async function gerar_personagem_com_base_em_historia(historia) {
  try {
    const response = await fetch(`${baseURL}/gerar_personagens_historia`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        historia: historia,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
}

/**
 * 
 * @param {string} propmpt 
 * @returns 
 */
async function gerar_historia_completa(propmpt) {
  try {
    debugger;
    const response = await fetch(`${baseURL}/gerar_historia_completa`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'allow-origin': '*',
        'acess-control-allow-origin': '*',
      },
      body: JSON.stringify({
        prompt: propmpt,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
}

export default {
  buscar_imagens,
  gerar_historia,
  gerar_personagem,
  gerar_monstro,
  gerar_local,
  gerar_personagem_com_base_em_historia,
  gerar_historia_completa,
};