# Description

It is a case study for Django REST micro service architecture with JWT authentication.<br>
Cookies are used for Token Read/Write operations.
<br>
<br>
<img src="https://github.com/ercan5535/Django-REST-Project-NGINX-JWT/assets/67562422/3ec9a303-a69f-48a9-94b3-79b6d3b5c4ff" width="500" height="400">
<br>

### API Gateway
- Serves static files
- Redirect reqeusts to relevant service

### Auth Service
- Responsible for User Register/Login/Logut and Create/Refresh/Store/Blacklist JWT.

### Transactions Service
- Responsible for CRUD operations.

### Redis Cache
- Caching (Tokens, UserData) pairs
- Caching JWT Access tokens for validation from Transaction Service
- Caching JWT Refresh tokens for blacklisting Refresh tokens
