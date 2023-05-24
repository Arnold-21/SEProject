import React, { useState } from "react"
import NavMenu from "./NavMenu"

export default function (props) {

  return (
    <div>
      <NavMenu/>
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Update Profile</h3>
          <div className="form-group mt-3">
            <label>First Name</label>
            <input
              type="first_name"
              className="form-control mt-1"
              placeholder="First Name"
            />
          </div>
          <div className="form-group mt-3">
            <label>Last Name</label>
            <input
              type="last_name"
              className="form-control mt-1"
              placeholder="Last Name"
            />
          </div>
          <div className="form-group mt-3">
              <label>Email address</label>
              <input
                type="email"
                className="form-control mt-1"
                placeholder="Enter email"
              />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              type="password"
              className="form-control mt-1"
              placeholder="Password"
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Update Account
            </button>
            <button type="submit" className="btn btn-primary">
              Delete Account
            </button>
          </div>
        </div>
      </form>
    </div>
    </div>
  )
}