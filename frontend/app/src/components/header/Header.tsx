import React from "react";
import AuthService from "../../services/authService";


const Header: React.FC<{ "handleJWT": CallableFunction; }> = (props) => {
    const logout = async () => {
        props.handleJWT("")
        await AuthService.logout()
    };


    return <div className="Header">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">To-Do App</a>
                <a className="link-light" href="#" onClick={() => logout()}>
                    {localStorage.getItem("JWT") ? "Log Out" : "Sign In"}
                </a>
            </div>
        </nav>
    </div>
};


export default Header
