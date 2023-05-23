import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";

export default function (props) {

  const [code, setCode] = useState("");

  const navigate = useNavigate();
  let location = useLocation();

  let currentId = location.state;
  let result = "empty";

  async function activate(event) {

    event.preventDefault();
    try {
        await axios.get("https://SE-Backend.strangled.net/api/register/confirm/" + code + "/" + currentId).then(function (response) {
          result = response.success;
          console.log(result);
      }).then(navigate("/main"));;
    } catch (err) {
        alert(err.error);
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
    </div>
  )
}