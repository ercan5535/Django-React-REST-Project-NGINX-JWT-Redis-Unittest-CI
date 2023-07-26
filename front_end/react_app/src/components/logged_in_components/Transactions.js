import React from 'react'

export default function Transactions({transactionData, setCurrentTransaction, setActivePage}){
  function handleClick(transaction){
    setActivePage('detail-transaction')
    setCurrentTransaction(transaction)
  }

  return(
      <div>
          <h1>All Transactions</h1>
          <br/>
          <table id="transactions_table" className="text-nowrap table table-secondary table-striped table-hover table-bordered table-sm">
              <caption>Hit ID to see/edit transaction details</caption>
              <thead className="table-dark" >
                  <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Department</th>
                  <th scope="col">Amount</th>
                  <th scope="col">Created By</th>
                  <th scope="col">Confirm Status</th>
                  <th scope="col">Created At</th>
                  </tr>
              </thead>
              <tbody>
                {transactionData.map((transaction) => {
                  return (
                    <tr key={transaction.id}>
                      <td><button onClick={() => handleClick(transaction)}>{transaction.id}</button></td>
                      <td>{transaction.department}</td>
                      <td>{transaction.amount}</td>
                      <td>{transaction.created_by}</td>
                      <td className={transaction.is_confirmed ? "confirmed" : "not-confirmed"}>
                        {transaction.is_confirmed ? "Confirmed" : "Not Confirmed"}
                      </td>
                      <td>{transaction.created_at}</td>
                    </tr>
                  )
                })}
              </tbody>
          </table> 
      </div>
  )
}