import React, {useEffect, useState} from 'react'
import LoggedInPage from './components/LoggedInPage'
import NotLoggedInPage from './components/NotLoggedInPage'

function App() {
  const [loginStatus, setLoginStatus] = useState(false)
  const [loading, setLoading] = useState(true)

  async function checkLoginStatus(){
    // first check access token
    const access_response = await fetch(
        'http://localhost:80/auth/api/authentication/check/', {
        method: 'GET',
        credentials: 'include',
      });
    if (access_response.ok){
      console.log('Access token is valid');
      const user_data = await access_response.json()
      localStorage.setItem("userData", JSON.stringify(user_data))
      setLoginStatus(true)
      setLoading(false)
      return
    }
    // second check refresh token
    const refresh_response = await fetch(
      'http://localhost:80/auth/api/authentication/refresh/', {
      method: 'GET',
      credentials: 'include',
    });
    if (refresh_response.ok){
      console.log('Refresh token is valid');
      const user_data = await refresh_response.json()
      localStorage.setItem("userData", JSON.stringify(user_data))
      setLoginStatus(true)
      setLoading(false)
    }
    else{
    // Display login page
    console.log("Both token are invalid")
    setLoginStatus(false)
    setLoading(false)
    }
  }

  useEffect(() => {
    checkLoginStatus()
  }, [])

  return (
    <div>
      {loading && <h1>Loading...</h1>}
      {!loading && !loginStatus && <NotLoggedInPage setLoginStatus={setLoginStatus}/>}
      {!loading && loginStatus && <LoggedInPage setLoginStatus={setLoginStatus}/>}
    </div>
  );
}

export default App;
