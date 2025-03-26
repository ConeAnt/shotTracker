import { useState, useEffect } from "react";
import { loadShootingLog, saveShootingLog } from "./utils/storage";
import Dashboard from "./components/Dashboard";
import LogSession from "./components/LogSession";
import Settings from "./components/Settings";

function App() {
  const [logs, setLogs] = useState([]);
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [targetArrows, setTargetArrows] = useState(localStorage.getItem("targetArrows") || "");

  useEffect(() => {
    setLogs(loadShootingLog());
  }, []);

  const addNewEntry = (newEntry) => {
    saveShootingLog(newEntry);
    setLogs(loadShootingLog()); // Refresh list
  };

  const saveSettings = (newUsername, newTargetArrows) => {
    setUsername(newUsername);
    setTargetArrows(newTargetArrows);
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