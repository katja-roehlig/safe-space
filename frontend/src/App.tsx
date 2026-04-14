import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingPage } from "./pages/LandingPage";
import { Register } from "./pages/Register";
import { NotFound } from "./pages/NotFound";
import { Login } from "./pages/Login";
import { Onboarding } from "./pages/Onboarding";
import { Chat } from "./pages/Chat";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        {/* Zur Registrierung */}
        <Route path="/register" element={<Register />} />

        {/* Zum Login */}
        <Route path="/login" element={<Login />} />

        {/* 404 Page */}
        <Route path="*" element={<NotFound />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </BrowserRouter>
  );
}
