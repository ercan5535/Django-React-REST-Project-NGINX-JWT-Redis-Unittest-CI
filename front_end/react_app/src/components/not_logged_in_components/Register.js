import React, {useState} from 'react'

export default function Register({setActivePage, setAlertMessage, setErrorMessage}){
    const [formData, setFormData] = useState(
        {
            email: "",
            password: "",
            password2: "",
            first_name: "",
            last_name: "",
            is_manager: false
        }
    )

    function handleChange(event) {
        const {name, value, type, checked} = event.target
        setFormData(prevFormData => {
            return {
                ...prevFormData,
                [name]: type === "checkbox" ? checked : value
            }
        })
    }

    async function handleSubmit(event){
        event.preventDefault()
        if (formData.password !== formData.password2){
            return setErrorMessage('Passwords not match')
        }

        var registerData = {
            "email": formData.email,
            "password": formData.password,
            "first_name": formData.first_name,
            "last_name": formData.last_name,
            "is_manager": formData.is_manager
          };
      
        // Convert the data object to a JSON string
        var jsonData = JSON.stringify(registerData);

        const register_response = await fetch(
            "http://localhost:80/auth/api/authentication/register/", {
            method: "POST",
            credentials: 'include',
            body: jsonData,
            headers: {
              "Content-Type": "application/json"
            }});
          if (register_response.ok){
            // Display login page
            setActivePage('login')
            setAlertMessage("Registered succesfully"); // Update alert message
          }
          else{
            const response_data = await register_response.text();
            setErrorMessage(response_data); // Update error message
          }
    }

    return (
        <form onSubmit={handleSubmit}>
          <h1>Register</h1>
          <div className="form-group">
            <label htmlFor="RegisterEmail">Email address</label>
            <input 
                type="email" 
                className="form-control" 
                id="RegisterEmail" 
                placeholder="Enter email"
                onChange={handleChange}
                name='email'
            />
          </div>
          <br/>
          <div className="form-group">
            <label htmlFor="RegisterPassword1">Password</label>
            <input 
                type="password" 
                className="form-control" 
                id="RegisterPassword1" 
                placeholder="Password"
                onChange={handleChange}
                name='password'
            />
          </div>
          <br/>
          <div className="form-group">
            <label htmlFor="RegisterPassword2">Password Confirmation</label>
            <input 
                type="password" 
                className="form-control" 
                id="RegisterPassword2" 
                placeholder="Password Confirmation" 
                onChange={handleChange}
                name='password2'
            />
          </div>
          <br/>
          <div className="form-group">
            <label htmlFor="RegisterFirstName">First Name</label>
            <input 
                type="text" 
                className="form-control" 
                id="RegisterFirstName" 
                placeholder="First Name"
                onChange={handleChange}
                name='first_name'
            />
          </div>
          <br/>
          <div className="form-group">
            <label htmlFor="RegisterLastname">Last Name</label>
            <input 
                type="text" 
                className="form-control" 
                id="RegisterLastname" 
                placeholder="Last Name"
                onChange={handleChange}
                name='last_name'
            />
          </div>
          <br/>
          <div className="form-check">
            <input 
                className="form-check-input" 
                type="checkbox"
                id="RegisterManagerCheck"
                onChange={handleChange}
                name='is_manager'
            />
            <label className="form-check-label" htmlFor="RegisterManagerCheck">
              Manager Account
            </label>
          </div>
          <br/>
          <button type="submit" className="btn btn-secondary">Register</button>
        </form>
    )
}