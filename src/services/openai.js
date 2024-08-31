export const fetchOpenAiData = async (prompt) => {
  const openAiApiKey = import.meta.env.VITE_OPENAI_API_KEY;

  try {
    const response = await fetch('https://api.openai.com/v1/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${openAiApiKey}`,
      },
      body: JSON.stringify({
        model: 'text-davinci-003', //TODO: ver se esse é o modelo certo
        prompt: prompt,
        max_tokens: 100,
      }),
    });

    const data = await response.json();
    return data.choices[0].text;
  } catch (error) {
    console.error('Erro ao chamar a API:', error);
    return null;
  }
};
