import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Auth from "./components/Auth"
import Recovery from "./components/Recovery"
import Activation from "./components/Activation"
import Profile from "./components/Profile"
import ClientMain from "./components/ClientMain"
import Admin from "./components/Admin"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/auth" element={<Auth />} />
        <Route path="/recover" element={<Recovery />} />
        <Route path="/activate" element={<Activation />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/main" element={<ClientMain />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
