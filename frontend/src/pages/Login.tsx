import { Link } from "react-router-dom";

export const Login = () => {
  return (
    <main>
      <h1>Logge dich ein</h1>
      <div>
        <label htmlFor="mail">Deine Mailadresse: </label>
        <input type="email" name="mail" id="mail" />
      </div>
      <div>
        <label htmlFor="password">Dein Passwort: </label>
        <input type="password" name="password" id="password" />
      </div>
      <button type="submit">Los geht´s</button>
      <br />
      <Link to="/">Home</Link>
      <br />
      <Link to="/">Registrieren</Link>
    </main>
  );
};
