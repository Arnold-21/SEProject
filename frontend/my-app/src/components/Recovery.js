import React, { useState } from "react"
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function (props) {

  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");

  const [userId, setUserId] = useState("");
  let navigate = useNavigate();

  async function firstPhase(event) {

    event.preventDefault();
    try {
        await axios.post("https://SE-Backend.strangled.net/api/recover/", {

            email: email,

        }).then(function (response) {
          setUserId(response.data.success);
          console.log(userId);
      });

    } catch (err) {
        toast(err.response.data.error);
    }
}

async function secondPhase(event) {

  event.preventDefault();
  try {
      await axios.put("https://SE-Backend.strangled.net/api/recover/" + code + "/" + userId + "/", {password: password} ).then(function (response) {
                console.log(response.data.success);
    });
    navigate("/");

  } catch (err) {
      toast(err.response.data.error);
  }
}

  return (
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Recover Account</h3>
          <div className="form-group mt-3">
              <label>Email address</label>
              <input
                type="email"
                className="form-control mt-1"
                placeholder="Enter email"
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary" onClick={firstPhase}>
              Send Recovery Code
            </button>
          </div>  
          <div className="form-group mt-3">
            <label>Recovery code</label>
            <input
              type="code"
              className="form-control mt-1"
              placeholder="Enter code"
              value={code}
              onChange={e => setCode(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>New Password</label>
            <input
              type="password"
              className="form-control mt-1"
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary" onClick={secondPhase}>
              Recover Account
            </button>
          </div>
          <p className="text-center mt-2">
              <a href="/auth">Back to login</a>
            </p>
        </div>
      </form>
      <ToastContainer />
    </div>
  )
}