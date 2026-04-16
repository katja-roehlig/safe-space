import { Link } from "react-router-dom";

export const Header = () => {
  return (
    <main>
      <h1>Serenity</h1>
      <nav>
        <Link to="/">Home</Link>
      </nav>
    </main>
  );
};
