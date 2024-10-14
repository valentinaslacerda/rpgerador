import { useState } from 'react';
import logo from './assets/book.svg';
import woods from './assets/woods.jpg';
import './App.css';
import { fetchOpenAiData } from './services/openai';
import apiService from './services/api';
import ReactMarkdown from 'react-markdown'
import ClipLoader from "react-spinners/ClipLoader";

const EditableSection = ({ type, content, onEdit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [inputText, setInputText] = useState('');

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleSaveClick = () => {
    onEdit(type, inputText);
    setIsEditing(false);
  };

  const toUpperCase = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  return (
    <div className="container">

      <h2>
        {type === 'ambientacao' ? 'Ambientação' : toUpperCase(type)}
      </h2>

      {type === 'ambientacao' ? (
        <div>
          <img src={woods} alt="Ambientação" className="ambientacao-image" />
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      ) : (
        <ReactMarkdown>{content}</ReactMarkdown>
      )}
      {isEditing ? (
        <div>
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Digite seu prompt aqui"
            className="edit-input"
          />
          <button onClick={handleSaveClick}>Salvar</button>
        </div>
      ) : (
        <button className="edite" onClick={handleEditClick}>
          Editar {type === 'ambientacao' ? 'Ambientação' : type}
        </button>
      )}
    </div>
  );
};

function App() {
  const [texto, setTexto] = useState('');
  const [response, setResponse] = useState([]);

  const [ambientacao, setAmbientacao] = useState(false);
  const [personagem, setPersonagem] = useState(false);
  const [monstro, setMonstro] = useState(false);
  const [historia, setHistoria] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleClickAmbientacao = () => {
    setAmbientacao(!ambientacao);
  }

  const handleClickPersonagem = () => {
    setPersonagem(!personagem);
  }

  const handleClickMonstro = () => {
    setMonstro(!monstro);
  }

  const handleClickHistoria = () => {
    setHistoria(!historia);
  }

  const handleSubmit = async () => {
    try {

      setLoading(true);

      const prompt = texto;

      debugger;

      if (!prompt) {
        alert('Digite algo para gerar a história');
        return;
      }

      if (!ambientacao && !personagem && !monstro && !historia) {
        alert('Selecione o que deseja gerar');
        return;
      }

      //gerar historia completa
      if (ambientacao && personagem && monstro && historia) {
        const result = await apiService.gerar_historia_completa(prompt);

        if (!result) {
          throw new Error('Erro ao buscar dados da API');
        }

        let content = result.premise + '\n\n' + result.outline + '\n\n' + result.story_text;
        content = content + '\n\n' + result.personagens + '\n\n' + result.monstros + '\n\n' + result.locais;

        setResponse((prevResponse) => [...prevResponse, { type: 'historia', content: content }]);
        return;
      }

      if (ambientacao) {
        const result = await apiService.gerar_local(prompt);

        if (!result) {
          throw new Error('Erro ao buscar dados da API');
        }

        setResponse((prevResponse) => [...prevResponse, { type: 'ambientacao', content: result.local }]);
      }

      if (personagem) {
        const result = await apiService.gerar_personagem(prompt);

        if (!result) {
          throw new Error('Erro ao buscar dados da API');
        }

        setResponse((prevResponse) => [...prevResponse, { type: 'personagem', content: result.personagem }]);
      }

      if (monstro) {
        const result = await apiService.gerar_monstro(prompt);

        if (!result) {
          throw new Error('Erro ao buscar dados da API');
        }

        setResponse((prevResponse) => [...prevResponse, { type: 'monstro', content: result.monstro }]);
      }

      if (historia) {
        const result = await apiService.gerar_historia(prompt);

        if (!result) {
          throw new Error('Erro ao buscar dados da API');
        }

        const content = result.premise + '\n\n' + result.outline + '\n\n' + result.story_text;

        setResponse((prevResponse) => [...prevResponse, { type: 'historia', content: content }]);
      }

    } catch (error) {
      console.error('Erro ao buscar dados da API:', error);
      alert('Erro ao buscar dados da API, tente novamente');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async (type, inputText) => {
    try {
      let prompt = `Refaça a história de RPG com o seguinte elemento: ${type}\n`;

      if (inputText) {
        prompt += `Texto adicional: ${inputText}\n`;
      }

      const result = await fetchOpenAiData(prompt);

      setResponse((prevResponse) =>
        prevResponse.map((item) =>
          item.type === type ? { ...item, content: result } : item,
        ),
      );
    } catch (error) {
      console.error('Erro ao buscar dados da API:', error);
    }
  };

  const submitTeste = async () => {
    const result = await apiService.gerar_historia('teste');
    console.log(result);
  }

  return (
    <>
      <div>
        <img src={logo} className="logo" alt="Logo" />
      </div>
      <h1>RPGERADOR</h1>
      <div className="card">

        <button
          onClick={handleClickAmbientacao}
          className={ambientacao ? 'clicked' : ''}
        >
          Ambientação
        </button>
        <button
          onClick={handleClickPersonagem}
          className={personagem ? 'clicked' : ''}
        >
          Personagem
        </button>
        
        <button
          onClick={handleClickMonstro}
          className={monstro ? 'clicked' : ''}
        >
          Monstro
        </button>

        <button
          onClick={handleClickHistoria}
          className={historia ? 'clicked' : ''}
        >
          História
        </button>
      </div>
      <div className="input-container">
        <input
          type="text"
          id="texto"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Digite Sobre o que é sua história aqui"
        />
        
        {loading ? 
          <ClipLoader color={'#BB8493'} loading={loading} size={150} />
          :
            <button 
              className="confirm" 
              onClick={handleSubmit}
            >
              Confirmar
            </button>
        }
        
      </div>
      <div className="response-container">
        {response.map(({ type, content }) => (
          <EditableSection
            key={type}
            type={type}
            content={content}
            onEdit={handleEdit}
          />
        ))}
      </div>
    </>
  );
}

export default App;
