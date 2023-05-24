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
import Logout from "./components/Logout"
import NothingToSeeHere from "./components/NothingToSeeHere"
import useToken from "./components/useToken"
import useRefresh from "./components/useRefresh"
import { useEffect, useState } from 'react'
import axios from 'axios'
import jwt_decode from "jwt-decode";

function App() {

  const { token, setToken } = useToken();
  const { refresh, setRefresh } = useRefresh();
  const [ adminAccess, setAdminAccess ] = useState(0);

  useEffect(() => {
    async function refreshTokens(){
      if(refresh)
      {
        try{
        const response = await axios.post('https://SE-Backend.strangled.net/api/token/refresh/', {refresh: refresh});
        setToken(response.data.access);
        }
        catch(err)
        {
          setToken("");
          setRefresh("");
        }
      }
    }
    const minute = 1000 * 60;
    refreshTokens();
    setInterval(refreshTokens, minute*3);
  }, []);

  useEffect(() => {
    if(token)
    {
      let decoded = jwt_decode(token);
        if(decoded.role != "Regular")
          setAdminAccess(1);
        else
          setAdminAccess(0);
    }
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ refresh ? <ClientMain  /> : <Auth />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/recover" element={<Recovery />} />
        <Route path="/activate" element={<Activation />} />
        <Route path="/user" element={<Profile />} />
        <Route path="/main" element={<ClientMain />} />
        <Route path="/admin" element={ adminAccess ? <Admin /> : <NothingToSeeHere/>} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
