import { useState } from 'react';
import logo from './assets/book.svg';
import woods from './assets/woods.jpg';
import './App.css';
import { fetchOpenAiData } from './services/openai';
import apiService from './services/api';

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

  return (
    <div className="container">
      {type === 'ambientacao' ? (
        <img src={woods} alt="Ambientação" className="ambientacao-image" />
      ) : (
        <p>{content}</p>
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
  const [selectedElements, setSelectedElements] = useState({
    ambientacao: false,
    personagem: false,
    monstro: false,
    trilha: false,
    historia: false,
  });
  const [texto, setTexto] = useState('');
  const [response, setResponse] = useState([]);

  const generatePrompt = () => {
    let prompt = 'Crie uma história de RPG com os seguintes elementos:\n';

    Object.keys(selectedElements).forEach((key) => {
      if (selectedElements[key])
        prompt += `- ${key.charAt(0).toUpperCase() + key.slice(1)}\n`;
    });

    if (texto) prompt += `Texto adicional: ${texto}\n`;

    return prompt;
  };

  const handleSubmit = async () => {
    try {
      const prompt = generatePrompt();
      const result = await fetchOpenAiData(prompt);

      let newResponse = [];

      Object.keys(selectedElements).forEach((key) => {
        if (selectedElements[key]) {
          newResponse.push({
            type: key,
            content: 'Lorem ipsum dolor sit amet...',
          });
        }
      });

      setResponse(newResponse);
    } catch (error) {
      console.error('Erro ao buscar dados da API:', error);
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
        {Object.keys(selectedElements).map((key) => (
          <button
            key={key}
            className={selectedElements[key] ? 'clicked' : ''}
            onClick={() =>
              setSelectedElements({
                ...selectedElements,
                [key]: !selectedElements[key],
              })
            }
          >
            {key.charAt(0).toUpperCase() + key.slice(1)}
          </button>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          id="texto"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Digite sua história aqui"
        />
        <button className="confirm" onClick={handleSubmit}>
          Confirmar
        </button>
        <button onClick={submitTeste}> teste </button>
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
