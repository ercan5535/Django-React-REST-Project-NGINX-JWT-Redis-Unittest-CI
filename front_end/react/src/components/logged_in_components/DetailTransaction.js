import React, {useState} from 'react'

export default function DetailTransaction({currentTransaction, setCurrentTransaction, setAlertMessage, setErrorMessage, setActivePage, setLoginStatus}){
    var USER_DATA = JSON.parse(localStorage.getItem("userData"))

    const [formData, setFormData] = useState(
        {
            department: currentTransaction.department,
            amount: currentTransaction.amount,
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

    async function updateTransaction(event){
        event.preventDefault()
        // Convert the data object to a JSON string
        var jsonData = JSON.stringify(formData);
        const update_transaction_response = await fetch(
            `http://localhost:80/transactions/api/transactions/detail/${currentTransaction.id}`, {
              method: "PATCH",
              credentials: 'include',
              body: jsonData,
              headers: {
                "Content-Type": "application/json"
              }
            });
          if (update_transaction_response.ok){
            // Create alert
            setAlertMessage("Transaction Updated Successfully!");
            setActivePage('transactions')
          }
          else if (update_transaction_response.status === 401){
            setLoginStatus(false)
          }
          else{
            const transaction_data = await update_transaction_response.text();
            setErrorMessage(transaction_data); // Update error message
          }
    }

    async function deleteTransaction(){
        const delete_transaction_response = await fetch(
            `http://localhost:80/transactions/api/transactions/detail/${currentTransaction.id}`, {
            method: "DELETE",
            credentials: 'include',
        });
        if (delete_transaction_response.ok){
            // Create alert
            setAlertMessage("Transaction Deleted Successfully!");
            setActivePage('transactions')
        }
        else if (delete_transaction_response.status === 401){
            setLoginStatus(false)
        }
        else{
            const transaction_data = await delete_transaction_response.text();
            setErrorMessage(transaction_data); // Update error message
        }
    }

    async function toggleConfirmation() {
        const confirm_transaction_response = await fetch(
            `http://localhost:80/transactions/api/transactions/detail/${currentTransaction.id}`, {
            method: "HEAD",
            credentials: 'include',
        });
        if (confirm_transaction_response.ok){
            setCurrentTransaction(prevTransaction => {
                return {
                    ...prevTransaction,
                    is_confirmed: !prevTransaction.is_confirmed
                }
            })
        }
        else if (confirm_transaction_response.status === 401){
            setLoginStatus(false)
        }
    }

    return(
        <div>
            <form onSubmit={updateTransaction}>
                <h1>Transaction Details</h1>
                <div className="form-group">
                    <label>Department</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        id="TransactionDetailDepartment" 
                        placeholder="Enter Department" 
                        name='department'
                        onChange={handleChange}
                        value={formData.department}
                    />
                </div>
                <br/>
                <div className="form-group">
                    <label>Amount</label>
                    <input 
                        type="number" 
                        step="0.01" 
                        className="form-control" 
                        id="TransactionDetailAmount" 
                        placeholder="Enter Amount"
                        name='amount'
                        onChange={handleChange}
                        value={formData.amount}
                    />
                </div>
                <br/>
                <div className="form-group">
                    <label>Confirm Status</label>
                    <input 
                        type="text" 
                        className={currentTransaction.is_confirmed ? "form-control confirmed" : "form-control not-confirmed"} 
                        id="TransactionDetailConfirmed" 
                        name='is_confirmed'
                        onChange={handleChange}
                        value={currentTransaction.is_confirmed ? "Confirmed" : "Not Confirmed"}
                        readOnly
                    />
                </div>
                <br/>
                <div className="form-group">
                    <label>Created By</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        id="TransactionDetailCreatedBy" 
                        name='created_by'
                        onChange={handleChange}
                        value={currentTransaction.created_by}
                        readOnly
                    />
                </div>
                <br/>
                <div className="form-group">
                    <label>Created At</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        id="TransactionDetailCreatedAt" 
                        name='created_at'
                        onChange={handleChange}
                        value={currentTransaction.created_at}
                        readOnly
                    />
                </div>
                <br/>
                <button type="submit" className="btn btn-secondary">Update Transaction</button>
            </form>
            <br/>
            <button type="button" onClick={deleteTransaction} className="btn btn-danger">Delete Transaction</button>
            <br/>
            <br/>
            {USER_DATA.is_manager && <button
                type="button" 
                onClick={toggleConfirmation}
                className={currentTransaction.is_confirmed ? "btn btn-danger" : "btn btn-success"}
                >
                {currentTransaction.is_confirmed ? "Disconfirm Transaction" : "Confirm Transaction"}
            </button>}
        </div>
    )
}