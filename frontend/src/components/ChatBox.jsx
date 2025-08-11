import React, { useState } from 'react';

function ChatBox({ onResponse }) {
  const [question, setQuestion] = useState("");

  const ask = async () => {
    const res = await fetch('http://localhost:5000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    const data = await res.json();
    onResponse(data);
  };

  return (
    <div>
      <input value={question} onChange={e => setQuestion(e.target.value)} />
      <button onClick={ask}>Ask</button>
    </div>
  );
}

export default ChatBox;
