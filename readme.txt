- Domin: http://fy19ayyn.pythonanywhere.com
- Admin:
	username: ammar
	password: 12345
- The implementation of the Airline company API is straightforward and easy to use. This API has been developed using the Django framework.
- Endpoints that can be accessed:
1. admin/
	Admin has full access to the database. They can change any tables, add, or delete.
	try: http://fy19ayyn.pythonanywhere.com/admin

2. api/flight/<int:id>
	This endpoint returns specific flight details (get)
	try:
	get: http://fy19ayyn.pythonanywhere.com/api/flight/1

3. api/flights
	This endpoint returns all flight that mach given data such as departure and destination airports (get)
	try:
	get: http://fy19ayyn.pythonanywhere.com/api/flights
	body:
	{
    		"departure_datetime": "2023-05-16T17:12:14Z",
    		"departure_airport": "Man Airport",
    		"destination_airport": "Oman Airport"
	}
	
4. api/paybooking/<int:booking_id>
	This endpoint create transaction id for a specific booking (post)
	try:
	post: http://fy19ayyn.pythonanywhere.com/api/paybooking/1
	body:
	{
    		"psp_id": "1"
	}

5. api/book
	This endpoint creates a booking in the database (post)
	try:
	post: http://fy19ayyn.pythonanywhere.com/api/book
	body:
	{
    		"flight": 1,
    		"payment_provider": 1,
    		"customer": {
        		"first_name": "Mhd",
        		"last_name": "Ammar",
        		"passport_number": "MA123",
        		"phone_number": "123505",
        		"email_address": "Mhd@no.com",
        		"date_of_birth": "1995-05-13",
        		"home_address": "Leeds"
    		}
	}

6. api/booking/<int:booking_id>
	This endpoint returns specific booking details (get) or change the details (put)
	try:
	get: http://fy19ayyn.pythonanywhere.com/api/booking/1
	or
	put: http://fy19ayyn.pythonanywhere.com/api/booking/1
	body:
	{
    		"customer": {
        		"customer_id": 1,
        		"first_name": "Ali",
   		      "last_name": "Siad",
        		"passport_number": "123",
        		"phone_number": "123",
        		"email_address": "alex@no.com",
        		"date_of_birth": "2023-05-16",
        		"home_address": "",
        		"allergies": ""
    		}
	}
	
7. api/confirmbooking
	This endpoint change booking status to confirmed if success key is right (put)
	try:
	put: http://fy19ayyn.pythonanywhere.com/api/confirmbooking
	body:
	{
    		"booking_id": 1,
    		"success_key": "confirmed"
	}

8. api/cancelbooking
	This endpoint change booking status to cancelled (put)
	try:
	put: http://fy19ayyn.pythonanywhere.com/api/cancelbooking
	body:
	{
    		"booking_id": 1
	}

9. api/paymentproviders
	This endpoint returns all PSPs available in this Airline company (get)
	try:
	get: http://fy19ayyn.pythonanywhere.com/api/paymentproviders