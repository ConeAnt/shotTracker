import React from "react";

const Dashboard = ({ logs }) => {
  return (
    <div>
      <h2>Dashboard</h2>
      <ul>
        {logs.length > 0 ? (
          logs.map((log, index) => (
            <li key={index}>
              {log.shoot_date} - {log.arrows_shot} arrows - Score: {log.perf_score}
            </li>
          ))
        ) : (
          <p>No shooting logs available.</p>
        )}
      </ul>
    </div>
  );
};

export default Dashboard;