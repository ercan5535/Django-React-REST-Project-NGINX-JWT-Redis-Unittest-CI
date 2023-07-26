export default function Navbar({setActivePage}){

    async function logout_request(){
        const logout_response = await fetch(
            "http://localhost:80/auth/api/authentication/logout/", {
            method: "GET",
            credentials: 'include',
        });
        if (logout_response.ok){
            // Reload page
            window.location.reload();
            // Delete user data from local storage
            localStorage.removeItem("userData")
        }
    }

    return(
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid">
                <a className="navbar-brand" href="">Django CRM</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                    <li className="nav-item">
                        <button onClick={() => {setActivePage('transactions')}}  className="nav-link">Transactions</button>
                    </li>
                        <li className="nav-item">
                        <button onClick={() => {setActivePage('new-transaction')}}  className="nav-link">Add Transaction</button>
                        </li>
                    </ul>
                </div>
                <div className="navbar-collapse collapse">
                    <ul className="navbar-nav ms-auto">
                    <li className="nav-item ml-auto">
                        <button onClick={() => {logout_request()}} className="nav-link">Logout</button>
                    </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}