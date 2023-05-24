import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function (props) {

  const [code, setCode] = useState("");

  const navigate = useNavigate();
  let location = useLocation();

  let currentId = location.state;

  async function activate(event) {

    event.preventDefault();
    try {
        await axios.get("https://SE-Backend.strangled.net/api/register/confirm/" + code + "/" + currentId + "/").then(function (response) {
      });
      navigate("/auth");
    } catch (err) {
        toast(err.response.data.error);
    }
}

  return (
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Activate Account</h3>
          <div className="form-group mt-3">
              <label>Activation Code</label>
              <input
                type="code"
                className="form-control mt-1"
                placeholder="Enter activation code"
                value={code}
                onChange={e => setCode(e.target.value)}
              />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary" onClick={activate}>
              Activate Account
            </button>
          </div>
        </div>
      </form>
      <ToastContainer />
    </div>
  )
}