import React, { useState } from "react"
import axios from "axios";
import useToken from "./useToken";
import { useNavigate } from "react-router-dom";

export default function (props) {
  let [authMode, setAuthMode] = useState("signin")

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin")
  }

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  let currentId = 0;
  let navigate = useNavigate();

  const { token, setToken } = useToken();

  async function login(event) {

    event.preventDefault();
    try {
        await axios.post("https://SE-Backend.strangled.net/api/token", {

            email: email,
            password: password,

        }).then(function (response) {
          setToken(response.access);
          console.log(response.access);
      });
      navigate("/main");

    } catch (err) {
        alert(err.detail);
    }
}

async function register(event) {

  event.preventDefault();
  try {
      await axios.post("https://SE-Backend.strangled.net/api/register", {

          first_name: firstName,
          last_name: lastName,
          password: password,
          email: email,

      }).then(function (response) {
        currentId = response.success;
        console.log(response.success);
    });
    navigate({
      pathname: '/activate',
        state: currentId // your data array of objects
    });

  } catch (err) {
      alert(err.response.data);
  }
}

  if (authMode === "signin") {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form">
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Sign In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeAuthMode}>
                Sign Up
              </span>
            </div>
            <div className="form-group mt-3">
            <label>Email address</label>
            <input
              type="email"
              className="form-control mt-1"
              placeholder="Email Address"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                className="form-control mt-1"
                placeholder="Enter password"
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary" onClick={login}>
                Submit
              </button>
            </div>
            <p className="text-center mt-2">
              Forgot <a href="/recover">password?</a>
            </p>
          </div>
        </form>
      </div>
    )
  }

  return (
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign Up</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="link-primary" onClick={changeAuthMode}>
              Sign In
            </span>
          </div>
          <div className="form-group mt-3">
            <label>First Name</label>
            <input
              type="first_name"
              className="form-control mt-1"
              placeholder="e.g Jane"
              value={firstName}
              onChange={e => setFirstName(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Last Name</label>
            <input
              type="last_name"
              className="form-control mt-1"
              placeholder="e.g Doe"
              value={lastName}
              onChange={e => setLastName(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Email address</label>
            <input
              type="email"
              className="form-control mt-1"
              placeholder="Email Address"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              type="password"
              className="form-control mt-1"
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary" onClick={register}>
              Submit
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}