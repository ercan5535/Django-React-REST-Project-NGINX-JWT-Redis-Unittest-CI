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
- JWT operations handled by jwt_helper.py

### Transactions Service
- Responsible for CRUD operations.
- Authenticate and Authorize(Only managers accounts can confirm Transactions) by checking tokens on cache

### Cache
- Holds (Tokens, UserData) pairs
- Holds JWT Access tokens for validation from Transaction Service
- Holds JWT Refresh tokens for blacklisting Refresh tokens
