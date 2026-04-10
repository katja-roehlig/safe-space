import { instance } from "../api/axios";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export const Register = () => {
  const [name, setName] = useState("");
  const [mail, setMail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const handleSubmit = async (event: React.SubmitEvent) => {
    event.preventDefault();
    try {
      const response = await instance.post("/register", {
        nickname: name,
        mail: mail,
        password: password,
      });
      console.log("Erfolg:", response.data);
      alert("Juhuu das hat geklappt");
      navigate("/login");
    } catch (error) {
      console.error(error);
      alert("Da ist etwas schief gelaufen");
    }
  };
  return (
    <main>
      <h1>Registriere dich hier!</h1>
      <form onSubmit={handleSubmit} method="post">
        <div>
          <label htmlFor="name">Wie möchtest du genannt werden? </label>
          <input
            type="text"
            name="name"
            id="name"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="mail">Deine Mailadresse: </label>
          <input
            type="email"
            name="mail"
            id="mail"
            value={mail}
            onChange={(event) => setMail(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Dein Passwort: </label>
          <input
            type="password"
            name="password"
            id="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
        <button type="submit">Registrieren</button>
      </form>
      <Link to="/">Home</Link>
    </main>
  );
};
