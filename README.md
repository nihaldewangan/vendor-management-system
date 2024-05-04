# vendor-management-system
Vendor Management System with Django Backend

Setup Instructions:

1. Make sure that python is installed (preferably 3.12).
2. Create a virtual environment using python.
3. Activate the virtual env.
4. Now, install the required dependencies listed in requirements file using the command "pip install -r requirements.txt" (Assuming the current path is same as the path where requirements.txt is located).
5. Apply the migrations with the command "python manage.py migrate" (if db.sqlite3 is absent).
6. If db.sqlite3 is absent, then run the command "python manage.py createsuperuser".
7. If db.sqlite3 is present, then username:nihal, password:qwerty.
8. Now, run the command "python manage.py runserver" to run the backend server.
Note: Here in this app, I have considered only single type of user and using the same credentials to create token.

API Instructions:

/api/login
    POST: Fetch a token for the user.
	example payload:
	{
		"username":<username>,
		"password":<password>
	}

	example response:
	{
		"token":<token>
	}

Note: 
1. In the apis below, Authorization Header needs to be sent with every request, in the given format: Authorization : Token <Token>
2. Fields marked with asterisk (*) are required fields.

/api/vendors/ (name='vendor')
    GET: Retrieve a list of all vendors.
    POST: Create a new vendor.
	sample payload:
	{
		"*name": "SS_AZ Retail", 
		"*contact_details": "7999079990",
		"*address": "Delhi",
		"*vendor_code": "1998",
		"on_time_delivery_rate":<on_time_delivery_rate>,
		"quality_rating_avg":<quality_rating_avg>,
		"average_response_time":<average_response_time>,
		"fulfillment_rate":<fulfillment_rate>
	}

	sample response:
	{
		"id":1, # vendor_id
	..............,
	..............,
	}


/api/vendors/<int:vendor_id>/
    GET: Retrieve details of a specific vendor.
    PUT: Update a specific vendor (partial details can be updated).
	sample payload:
	{
		"name": "SSD", 
		"contact_details": "9999079990",
		"address": "Mumbai",
		"on_time_delivery_rate":<on_time_delivery_rate>,
		"quality_rating_avg":<quality_rating_avg>,
		"average_response_time":<average_response_time>,
		"fulfillment_rate":<fulfillment_rate>
	}
	
    DELETE: Delete a specific vendor.


/api/purchase_orders/
    GET: Retrieve a list of all purchase orders.
    POST: Create a new purchase order.
	sample payload:
	{
		"*vendor": 7,
    		"*order_date": "2024-04-30T10:00:00Z",
    		"*delivery_date": "2024-05-15T10:00:00Z",
    		"*items": [
      		{
        		"name": "Product A",
        		"description": "Description of Product A",
        		"unit_price": 10.99,
        		"quantity": 100
      		},
      		{
        		"name": "Product B",
        		"description": "Description of Product B",
        		"unit_price": 8.50,
        		"quantity": 50
      		}
    	],
		"status":"pending",
		"quality_rating":6,
    		"*quantity": 150,
    		"*issue_date": "2024-04-30T10:00:00Z"
  	}

	sample response:
	{
		"id":1 # po_id
	..............,
	..............,
	}


/api/purchase_orders/<int:po_id>/
    GET: Retrieve details of a specific purchase order.
    PUT: Update a specific purchase order (partial details can be updated).
	sample payload:
	{
		"status":"pending", # options: ["pending", "completed", "canceled"]
		"quality_rating":6,
  	}
    DELETE: Delete a specific purchase order.


/api/vendors/<int:vendor_id>/performance/
    GET: Retrieve the performance data for a specific vendor.


/api/purchase_orders/<int:po_id>/acknowledge/
    POST: Acknowledge a specific purchase order by the vendor.


