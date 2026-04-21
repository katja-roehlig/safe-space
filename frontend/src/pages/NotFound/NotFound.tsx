import { Link } from "react-router-dom";

export const NotFound = () => {
  return (
    <>
      <h1>Seite existiert nicht</h1>
      <p>404 Error</p>
      <Link to="/">Zurück zur Startseite</Link>
    </>
  );
};
