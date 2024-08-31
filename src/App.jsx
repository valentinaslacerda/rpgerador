import { useState } from 'react';
import logo from './assets/book.svg';
import './App.css';
import { fetchOpenAiData } from './services/openai';

function App() {
  const [ambientacao, setAmbientacao] = useState(false);
  const [personagem, setPersonagem] = useState(false);
  const [monstro, setMonstro] = useState(false);
  const [trilha, setTrilha] = useState(false);
  const [historia, setHistoria] = useState(false);
  const [texto, setTexto] = useState('');
  const [confirmar, setConfirmar] = useState(false);
  const [response, setResponse] = useState('');

  const generatePrompt = () => {
    let prompt = 'Crie uma história de RPG com os seguintes elementos:\n';

    if (ambientacao) prompt += '- Ambientação\n';
    if (personagem) prompt += '- Personagem\n';
    if (monstro) prompt += '- Monstro\n';
    if (trilha) prompt += '- Trilha sonora\n';
    if (historia) prompt += '- História base\n';

    if (texto) prompt += `Texto adicional: ${texto}\n`;

    return prompt;
  };

  const handleSubmit = async () => {
    const prompt = generatePrompt();
    const result = await fetchOpenAiData(prompt);
    setResponse(result);
  };

  return (
    <>
      <div>
        <img src={logo} className="logo" alt="Logo" />
      </div>
      <h1>RPGERADOR</h1>
      <div className="card">
        <button
          className={ambientacao ? 'clicked' : ''}
          onClick={() => setAmbientacao(!ambientacao)}
        >
          Ambientação {ambientacao.toString()}
        </button>

        <button
          className={personagem ? 'clicked' : ''}
          onClick={() => setPersonagem(!personagem)}
        >
          Personagem {personagem.toString()}
        </button>

        <button
          className={monstro ? 'clicked' : ''}
          onClick={() => setMonstro(!monstro)}
        >
          Monstro {monstro.toString()}
        </button>

        <button
          className={trilha ? 'clicked' : ''}
          onClick={() => setTrilha(!trilha)}
        >
          Trilha {trilha.toString()}
        </button>

        <button
          className={historia ? 'clicked' : ''}
          onClick={() => setHistoria(!historia)}
        >
          História {historia.toString()}
        </button>
      </div>
      <div className="input-container">
        <input
          type="text"
          id="texto"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Adicione texto adicional..."
        />
        <button className="confirm" onClick={handleSubmit}>
          Confirmar
        </button>
      </div>
      <div className="response-container">
        <h2>Resposta:</h2>
        <p>{response}</p>
      </div>
    </>
  );
}

export default App;
