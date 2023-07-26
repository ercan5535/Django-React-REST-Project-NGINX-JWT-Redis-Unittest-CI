import React, {useState} from 'react'

export default function NewTransaction({setAlertMessage, setLoginStatus, setActivePage, setErrorMessage}){
    const [formData, setFormData] = useState(
        {
            department: "",
            amount: "",
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
        var USER_DATA = JSON.parse(localStorage.getItem("userData"))

        var newTransactionData = {
            department: formData.department,
            amount: formData.amount,
            created_by: USER_DATA.first_name + " " + USER_DATA.last_name
          };
      
        // Convert the data object to a JSON string
        var jsonData = JSON.stringify(newTransactionData);

        const new_transaction_response = await fetch(
            "http://localhost:80/transactions/api/transactions/transactions/", {
            method: "POST",
            credentials: 'include',
            body: jsonData,
            headers: {
              "Content-Type": "application/json"
            }});
        console.log(new_transaction_response)
        if (new_transaction_response.ok){
            setAlertMessage("New Transaction Added Successfully!");
            setActivePage('transactions')
        }
        else if (new_transaction_response.status === 401){
            setLoginStatus(false)
        }
        else{
            const transaction_data = await new_transaction_response.text();
            setErrorMessage(transaction_data); // Update error message
          }
    }

    return (
        <form onSubmit={handleSubmit}>
          <h1>Add Transaction</h1>
          <div className="form-group">
            <label htmlFor="NewTransactionDepartment">Department</label>
            <input 
                type="text" 
                className="form-control" 
                id="NewTransactionDepartment" 
                placeholder="Enter Department"
                onChange={handleChange}
                name='department'
            />
          </div>
          <br/>
          <div className="form-group">
            <label htmlFor="NewTransactionAmount">Amount</label>
            <input 
                type="number"
                step="0.01"
                className="form-control" 
                id="NewTransactionAmount" 
                placeholder="Enter Amount"
                onChange={handleChange}
                name='amount'
            />
          </div>
          <br/>
          <button type="submit" className="btn btn-secondary">Add Transaction</button>
        </form>
    )
}