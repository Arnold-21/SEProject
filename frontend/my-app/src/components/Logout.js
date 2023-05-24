import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import NavMenu from "./NavMenu"
import useToken from './useToken';
import useRefresh from './useRefresh';

export default function (props) {

    const { token, setToken } = useToken();
    const { refresh, setRefresh } = useRefresh();

    let navigate = useNavigate();

    async function logout(event) {

        event.preventDefault();

        setToken("");
        setRefresh("");

        navigate("/auth");
      }

  return (
    <div >
    <NavMenu/>
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Are you sure you want to log out?</h3>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary" onClick={logout}>
              Log Out
            </button>
          </div>
        </div>
      </form>
    </div>
    </div>
  )
}