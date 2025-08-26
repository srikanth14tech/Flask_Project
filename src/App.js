import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Call Flask API
    axios.get("http://127.0.0.1:5000/api/hello")
      .then((res) => {
        setMessage(res.data.message);
      })
      .catch((err) => {
        console.error("Error connecting to Flask API:", err);
      });
  }, []);

  return (
    <div>
      <h1>React + Flask Integration</h1>
      <p>Message from Flask: {message}</p>
    </div>
  );
}

export default App;
