import React, { useState } from "react"

export default function (props) {

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
              />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Send Recovery Code
            </button>
          </div>  
          <div className="form-group mt-3">
            <label>Recovery code</label>
            <input
              type="code"
              className="form-control mt-1"
              placeholder="Enter code"
            />
          </div>
          <div className="form-group mt-3">
            <label>New Password</label>
            <input
              type="password"
              className="form-control mt-1"
              placeholder="Password"
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Recover Account
            </button>
          </div>
          <p className="text-center mt-2">
              <a href="/auth">Back to login</a>
            </p>
        </div>
      </form>
    </div>
  )
}