import { Link } from "react-router-dom";

export const LandingPage = () => {
  return (
    <main>
      <h1>Willkommen bei SafeSpace</h1>
      <p>Schön, dass du hier bist!</p>
      <p>Wie möchtest du forfahren?</p>
      <nav>
        <Link to="/login">Einloggen</Link>
        <br />
        <Link to="/register">Registrieren</Link>
        <br />
        <Link to="/onboarding">Onboarding</Link>
      </nav>
    </main>
  );
};
