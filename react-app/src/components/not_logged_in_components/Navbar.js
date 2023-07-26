export default function Navbar({setActivePage}){

    return(
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid">
                <a className="navbar-brand" href="/">Django CRM</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <button onClick={() => {setActivePage('login')}} className="nav-link">Login</button>
                        </li>
                        <li className="nav-item">
                            <button onClick={() => {setActivePage('register')}} className="nav-link">Register</button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}