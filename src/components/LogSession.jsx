import React, { useState } from "react";

const LogSession = ({ onAddEntry }) => {
  const [arrowsShot, setArrowsShot] = useState("");
  const [perfScore, setPerfScore] = useState("");
  const [notes, setNotes] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!arrowsShot || !perfScore) return;

    onAddEntry({
      shoot_date: new Date().toISOString().split("T")[0],
      week_number: new Date().getWeekNumber(),
      arrows_shot: parseInt(arrowsShot, 10),
      perf_score: Math.min(10, parseInt(perfScore, 10)), // Max score 10
      notes,
    });

    setArrowsShot("");
    setPerfScore("");
    setNotes("");
  };

  return (
    <div>
      <h2>Log New Session</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Arrows Shot"
          value={arrowsShot}
          onChange={(e) => setArrowsShot(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Performance Score (max 10)"
          value={perfScore}
          onChange={(e) => setPerfScore(e.target.value)}
          required
          max={10}
        />
        <input
          type="text"
          placeholder="Notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
        <button type="submit">Add Session</button>
      </form>
    </div>
  );
};

export default LogSession;