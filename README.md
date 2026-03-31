# User-Service
## Vorbereitung

- Es muss eine .env-Datei angelegt werden. In .env.example ist ein Beispiel, wie diese aussehen muss. 
Es muss die Datenbankdetails und der Connection-String von Application Insights angegeben werden.


- Es braucht einen Public- und einen Privatekey. Der Public Key muss auch im API-gateway hinterlegt werden.
	-  `openssl genrsa -out private.pem 2048`
	-  `openssl rsa -in private.pem -pubout > public.pem`



func azure functionapp publish baju0afafcuserserv0dev --python


## Local testen
`uvicorn api.__init__:app --reload --port 8080`


## Als Azure Function deployen

`func azure functionapp publish <function-name> --python`