import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api/axios";

export const Login = () => {
  const [mail, setMail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event: React.SubmitEvent) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("username", mail); // Wichtig: FastAPI erwartet'username'
    formData.append("password", password);

    try {
      const response = await api.post("/login", formData);
      const token: string = response.data.access_token;
      localStorage.setItem("token", token);
      console.log("Erfolg:", response.data);
      if (response.data.has_onboarding) {
        navigate("/login"); //nur vorläufig zum Testen
      } else {
        navigate("/register"); //nur vorläufig zum Testen
      }
      alert("Du wurdest erfolgreich eingeloggt!");
    } catch (error) {
      console.error("Login fehlgeschlagen:", error);
      alert("Da ist etwas schief gelaufen");
    }
  };
  return (
    <main>
      <h1>Logge dich ein</h1>
      <form onSubmit={handleSubmit}>
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
        <button type="submit">Los geht´s</button>
      </form>
      <br />
      <Link to="/">Home</Link>
      <br />
      <Link to="/">Registrieren</Link>
    </main>
  );
};
