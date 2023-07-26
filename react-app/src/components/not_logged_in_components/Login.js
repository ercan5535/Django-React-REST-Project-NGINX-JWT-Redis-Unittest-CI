import React, {useState} from 'react'

export default function Login({setErrorMessage, setLoginStatus}){
    const [formData, setFormData] = useState(
        {
            email: "",
            password: "",
        }
    )

    function handleChange(event) {
        const {name, value} = event.target
        setFormData(prevFormData => {
            return {
                ...prevFormData,
                [name]: value
            }
        })
    }

    async function handleSubmit(event){
        event.preventDefault()
        // Convert the data object to a JSON string
        var jsonData = JSON.stringify(formData);

        const login_response = await fetch(
            "http://localhost:80/auth/api/authentication/login/", {
            method: "POST",
            credentials: 'include',
            body: jsonData,
            headers: {
                "Content-Type": "application/json"
            }
        });
        console.log(login_response)
        if (login_response.ok){
            const userData = await login_response.json()
            localStorage.setItem("userData", JSON.stringify(userData))
            setLoginStatus(true)
        }
        else{
            const response_data = await login_response.text();
            setErrorMessage(response_data); // Update error message
        }
    }

    return (
        <form onSubmit={handleSubmit}>
          <h1>Login</h1>
          <div className="form-group">
            <label htmlFor="LoginEmail">Email address</label>
            <input 
                type="email" 
                className="form-control" 
                id="LoginEmail" 
                placeholder="Enter email"
                onChange={handleChange}
                name='email'
            />
          </div>
          <br/>
          <div className="form-group">
            <label htmlFor="LoginPassword1">Password</label>
            <input 
                type="password" 
                className="form-control" 
                id="LoginPassword1" 
                placeholder="Password"
                onChange={handleChange}
                name='password'
            />
          </div>
          <br/>
          <button type="submit" className="btn btn-secondary">Login</button>
        </form>
    )
}