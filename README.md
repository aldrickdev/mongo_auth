# mongo_auth

This project is a simple API that provides basic Authentication and Authorization.

## Endpoints

`POST /api/v1/user/create` . 
Endpoint used to create a user and returns the users token.

``` python
# Request
data_in_request = {
    "username": "greymint",
    "email": "aldrick@greymint.com",
    "password": "password1234",
    "date_created": "date and time",
    "disabled": false,
    "role": "admin"
}

# Response
data_in_response = {
   "username": "greymint",
   "email": "aldrick@greymint.com",
   "disabled": false,
   "role": "admin" 
}
```

`POST /api/v1/user/login`  
Endpoint used to get a new token from the user credentials provided.

``` python
# Requests
data_in_request_username = {
    "username": "greymint",
    "password": "password1234",
}

data_in_request_email = {
    "email": "aldrick@greymint.com",
    "password": "password1234",
}

# Response
data_in_response = {
   "username": "greymint",
   "email": "aldrick@greymint.com",
   "disabled": false,
   "role": "admin" ,
   "token": "niuh1uibdsbfoisdfs",
}
```

`PUT /api/v1/user/edit`  
Endpoint used to update the users profile details

``` python
# Requests - Token in the header
data_in_request = {
    # Whatever you want to update: username, email, password
}

# Response
data_in_response = {
   "username": "greymint",
   "email": "aldrick@greymint.com",
   "disabled": false,
   "role": "admin" 
}
```

`GET /api/v1/user/profile`   
Endpoint used to get user details

``` python
# Requests - Token in the header
data_in_request = {
}

# Response
data_in_response = {
   "username": "greymint",
   "email": "aldrick@greymint.com",
   "disabled": false,
   "role": "admin" 
}
```

`PUT /api/v1/user/disable`  
Endpoint used to disable a user

``` python
# Requests - Token in the header
data_in_request = {
}

# Response
data_in_response = {
   "username": "greymint",
   "email": "aldrick@greymint.com",
   "disabled": true,
   "role": "admin" 
}
```
