export const loadShootingLog = () => {
    const data = localStorage.getItem("shooting_log");
    return data ? JSON.parse(data) : [];
  };
  
  export const saveShootingLog = (newEntry) => {
    const logs = loadShootingLog();
    logs.push(newEntry);
    localStorage.setItem("shooting_log", JSON.stringify(logs));
  };