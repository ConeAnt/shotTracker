import { useState, useEffect } from "react";
import { loadShootingLog, saveShootingLog } from "./utils/storage";
import Dashboard from "./components/Dashboard";
import LogSession from "./components/LogSession";
import Settings from "./components/Settings";

function App() {
  const [logs, setLogs] = useState([]);
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [targetArrows, setTargetArrows] = useState(localStorage.getItem("targetArrows") || "");

  // Load shooting logs when the component mounts
  useEffect(() => {
    setLogs(loadShootingLog());
  }, []);

  // Function to add a new entry to the shooting log
  const addNewEntry = (newEntry) => {
    saveShootingLog(newEntry);
    setLogs(loadShootingLog()); // Refresh list
  };

  // Function to save user settings
  const saveSettings = (newUsername, newTargetArrows) => {
    setUsername(newUsername);
    setTargetArrows(newTargetArrows);

    // Store settings in localStorage
    localStorage.setItem("username", newUsername);
    localStorage.setItem("targetArrows", newTargetArrows);
  };

  return (
    <div>
      <h1>Shooting Log Tracker</h1>
      <Settings onSaveSettings={saveSettings} />
      <LogSession onAddEntry={addNewEntry} />
      <Dashboard logs={logs} />
    </div>
  );
}

export default App;