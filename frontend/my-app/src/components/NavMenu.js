import React, { Component, useEffect, useState } from 'react';
import { Collapse, Navbar, NavbarBrand, NavbarToggler, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';
import './NavMenu.css';
import jwt_decode from "jwt-decode";
import useToken from './useToken';

export default function NavMenu() {

  
    const { token, setToken } = useToken();
    const [decoded, setDecoded] = useState({});

    useEffect(() => {
        if(token)
        setDecoded(jwt_decode(token));
      }, []);

    return (
      <header>
        <Navbar className="navbar-expand-sm navbar-toggleable-sm ng-white border-bottom box-shadow mb-3" container light>
          <NavbarBrand tag={Link} to="/main">Bucket App</NavbarBrand>
            <ul className="navbar-nav flex-grow">
              <NavItem>
                <NavLink tag={Link} className="text-dark" to="/main">Main</NavLink>
              </NavItem>
              <NavItem>
                <NavLink tag={Link} className="text-dark" to="/user">Update User</NavLink>
              </NavItem>
              {decoded?.role != "Regular" && 
              <NavItem>
                <NavLink tag={Link} className="text-dark" to="/admin">Admin Menu</NavLink>
              </NavItem>
              }
              <NavItem>
                <NavLink tag={Link} className="text-dark" to="/logout">Logout</NavLink>
              </NavItem>
            </ul>
        </Navbar>
      </header>
    );
}
