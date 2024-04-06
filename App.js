import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client'

function App() {
  const [gameData, setGameData] = useState({
    score: 0,
    time: 30,
    balloon_position: { x: 0, y: 0 }
  });

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/game_data');
      const data = await response.json();
      setGameData(data);
    };

    fetchData();
    const interval = setInterval(fetchData, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>Balloon Pop</h1>
      <div className="GameArea">
        <div className="Score">Score: {gameData.score}</div>
        <div className="Time">Time: {gameData.time}</div>
        <div className="Balloon" style={{ top: gameData.balloon_position.y, left: gameData.balloon_position.x }}></div>
      </div>
    </div>
  );
}

const root=ReactDOM.createRoot(document.getElementById("root"));
root.render(<App/>)
