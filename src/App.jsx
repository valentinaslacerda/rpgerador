import { useState } from 'react';
import logo from './assets/book.svg';
import './App.css';

function App() {
  const [ambientacao, setAmbientacao] = useState(false);
  const [personagem, setPersonagem] = useState(false);
  const [monstro, setMonstro] = useState(false);
  const [trilha, setTrilha] = useState(false);
  const [historia, setHistoria] = useState(false);
  const [texto, setTexto] = useState('');
  const [confirmar, setConfirmar] = useState(false);

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
          ambientação {ambientacao.toString()}
        </button>

        <button
          className={personagem ? 'clicked' : ''}
          onClick={() => setPersonagem(!personagem)}
        >
          personagem {personagem.toString()}
        </button>

        <button
          className={monstro ? 'clicked' : ''}
          onClick={() => setMonstro(!monstro)}
        >
          monstro {monstro.toString()}
        </button>

        <button
          className={trilha ? 'clicked' : ''}
          onClick={() => setTrilha(!trilha)}
        >
          trilha {trilha.toString()}
        </button>

        <button
          className={historia ? 'clicked' : ''}
          onClick={() => setHistoria(!historia)}
        >
          historia {historia.toString()}
        </button>
      </div>
      <div className="input-container">
        <input
          type="text"
          id="texto"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
        />
        <button className="confirm" onClick={() => setConfirmar(true)}>
          Confirmar
        </button>
      </div>
    </>
  );
}

export default App;
