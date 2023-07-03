# Description

It is a case study for Django REST micro service architecture with JWT authentication.<br>
Cookies are used for Token operations.
<br>
<br>
<div align="center">
  <img src="https://github.com/ercan5535/Django-REST-Project-NGINX-JWT/assets/67562422/3ec9a303-a69f-48a9-94b3-79b6d3b5c4ff" width="500" height="400">
</div>
<br>

### API Gateway
- Serves static files
- Redirects reqeusts to relevant service

### Auth Service
- Responsible for User Register/Login/Logut
- Responsible for Create/Refresh/Store/Blacklist JWT
- JWT parameters defined on settings.py
```
JWT = {
  "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
  "ALGORITHM": "HS256",
  "SIGNING_KEY": "MY_SIGNING_KEY_123",
}
```
- JWT operations handled by jwt_helper.py

### Transactions Service
- Responsible for CRUD operations.
- Authenticate and Authorize(Only managers accounts can confirm Transactions) by checking tokens on cache

### Cache
- Holds (Token, UserData) pairs
- Holds JWT Access tokens for validation from Transaction Service
- Holds JWT Refresh tokens for blacklisting Refresh tokens

### Front-End
- It is a simple single page application
- Login, Register, All Transactions, Add Transaction and Transaction Details Pages are available
- Update, Delete, Confirm operations are can be done on Transaction Details Page

# Usage
```
docker-compose up 
```
command is enough to run all services <br>
NGINX will listen localhost:80 for serving home page
