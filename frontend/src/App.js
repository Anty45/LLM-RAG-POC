import logo from './logo.svg';
import './App.css';
import queryIndex from './query_law.js'
import { useState } from 'react';
import { ReactComponent as Loader } from './loader.svg'


function App() {
    const [question, setQuestion] = useState('Posez votre question...');
    const [llmAnswer, setLlmAnswer] = useState("Votre réponse s'affichera ici...");
    const [showLoader, setShowLoader] = useState(false);
    const onSubmit = () => {
    console.log("ici")
    setShowLoader(true)
    queryIndex(question).then((response) => {
        setShowLoader(false);
        setLlmAnswer(response.answer);
      }).catch(rejected => {
        setShowLoader(false);
        console.log(rejected)
      });
    }

    return (
    <div className="App">
        <h1 className="App-header">
            GAJA explainer
        </h1>
        <label className="App-search-bar-component">
            <textarea
                className= "App-search-bar"
                value={question}
                onChange={e => setQuestion(e.target.value)}
            />
        </label>
        <button
            className="App-submit-btn"
            onClick={onSubmit}
            disabled={showLoader}
            >
                {!showLoader ? "ask" : <Loader className="App-submit-spinner" />}
        </button>

        <label className="App-llm-answer-bar-component">
            <textarea
                readonly
                className= "App-search-bar"
                value={llmAnswer}
            />
        </label>
    </div>
  );
}

export default App;
