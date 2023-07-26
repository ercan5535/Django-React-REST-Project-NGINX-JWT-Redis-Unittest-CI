import React, {useState} from 'react'
import Navbar from "./not_logged_in_components/Navbar"
import Login from "./not_logged_in_components/Login"
import Register from "./not_logged_in_components/Register"

export default function NotLoggedInPage({setLoginStatus}) {
    //pages: login, register
    const [activePage, setActivePage] = useState('login');
    const [alertMessage, setAlertMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const resetMessages = () => {
        setAlertMessage('');
        setErrorMessage('');
    };

    return (
        <main onClick={resetMessages}>
            <Navbar 
                setActivePage={setActivePage} />
            <div className="col-md-6 offset-md-3">
                <br />
                {alertMessage && <div className="alert alert-secondary" role="alert">{alertMessage}</div>}
                <br />
                {errorMessage && <div className='error-message'>{errorMessage}</div>}
                {activePage === 'login' && <Login 
                    setActivePage={setActivePage} 
                    setAlertMessage={setAlertMessage} 
                    setErrorMessage={setErrorMessage}
                    setLoginStatus={setLoginStatus}
                />}
                {activePage === 'register' && <Register 
                    setActivePage={setActivePage} 
                    setAlertMessage={setAlertMessage} 
                    setErrorMessage={setErrorMessage}
                />}
            </div>
        </main>
    )
}