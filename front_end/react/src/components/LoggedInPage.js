import React, {useState, useEffect} from 'react'

import Navbar from './logged_in_components/Navbar'
import Transactions from './logged_in_components/Transactions'
import NewTransaction from './logged_in_components/NewTransaction'
import DetailTransaction from './logged_in_components/DetailTransaction'


export default function NotLoggedInPage({setLoginStatus}) {
    //pages: transactions, new-transaction, detail-transaction
    const [activePage, setActivePage] = useState('transactions');
    const [alertMessage, setAlertMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [transactionData, setTransactionData] = useState([]);
    const [currentTransaction, setCurrentTransaction] = useState({});

    const resetMessages = () => {
        setAlertMessage('');
        setErrorMessage('');
    };

    async function getTransactionsData(){
        const get_transactions_response = await fetch(
          "http://localhost:80/transactions/api/transactions/transactions/", {
          method: "GET",
          credentials: 'include',
        });
        if (get_transactions_response.ok){
          // Create alert
          const transaction_data = await get_transactions_response.json()
          setTransactionData(transaction_data)
        }
        else if (get_transactions_response.status === 401){
          setLoginStatus(false)
        }
      }
  
    useEffect(() => {
        if (activePage === 'transactions'){
            getTransactionsData()
        }
    }, [activePage])

    return (
        <main onClick={resetMessages}>
            <Navbar 
                setActivePage={setActivePage} />
            <div className="col-md-6 offset-md-3">
                <br />
                {alertMessage && <div className="alert alert-secondary" role="alert">{alertMessage}</div>}
                <br />
                {errorMessage && <div className='error-message'>{errorMessage}</div>}
                {activePage === 'transactions' && <
                    Transactions 
                    transactionData={transactionData} 
                    setActivePage={setActivePage} 
                    setCurrentTransaction={setCurrentTransaction}/
                >} 
                {activePage === 'new-transaction' && <
                    NewTransaction 
                    setLoginStatus={setLoginStatus}
                    setActivePage={setActivePage} 
                    setAlertMessage={setAlertMessage}
                    setErrorMessage={setErrorMessage}
                />} 
                {activePage === 'detail-transaction' && <
                    DetailTransaction 
                    setLoginStatus={setLoginStatus}
                    setActivePage={setActivePage} 
                    setAlertMessage={setAlertMessage}
                    currentTransaction={currentTransaction}
                    setCurrentTransaction={setCurrentTransaction}
                    setErrorMessage={setErrorMessage}
                />} 
            </div>
        </main>
    )
}