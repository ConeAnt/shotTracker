import React, { useState, useEffect } from "react";

const Settings = ({ onSaveSettings }) => {
  const [username, setUsername] = useState("");
  const [targetArrows, setTargetArrows] = useState("");

  useEffect(() => {
    const savedUsername = localStorage.getItem("username");
    const savedTargetArrows = localStorage.getItem("targetArrows");

    if (savedUsername) setUsername(savedUsername);
    if (savedTargetArrows) setTargetArrows(savedTargetArrows);
  }, []);

  const handleSave = () => {
    localStorage.setItem("username", username);
    localStorage.setItem("targetArrows", targetArrows);
    onSaveSettings(username, targetArrows);
  };

  return (
    <div>
      <h2>Settings</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="number"
        placeholder="Annual Target Arrows"
        value={targetArrows}
        onChange={(e) => setTargetArrows(e.target.value)}
      />
      <button onClick={handleSave}>Save Settings</button>
    </div>
  );
};

export default Settings;