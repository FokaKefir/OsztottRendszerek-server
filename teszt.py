#   CREATE


# import requests
#
# url = 'http://localhost:3001/create_form'
# auth_token = 'token'
# form_data = {
#     "title": "Example Form",
#     "desc": "This is an example form.",
#     "opt": ["Option 1", "Option 2", "Option 3"]
# }
#
# params = {
#     'auth': auth_token
# }
#
# response = requests.post(url, json=form_data, params=params)
#
# # Check response
# if response.status_code == 200:
#     print("Form created successfully. Form ID:", response.json()["form_id"])
# elif response.status_code == 401:
#     print("Unauthorized access:", response.json().get("error", "Unknown error"))
# elif response.status_code == 422:
#     print("Validation error:", response.json().get("detail", "Validation error"))
#     print("Details:", response.content)
# else:
#     print("Error:", response.status_code, response.json())


#   SUBMISSION


# import requests
#
# # Endpoint URL
# url = 'http://localhost:8000/get_form_submission'
#
# auth_token = "token"
# form_id = "form1"
#
# params = {
#     "auth": auth_token,
#     "form_id": form_id,
# }
#
# # Making the GET request
# response = requests.get(url, params=params)
#
# # Checking the response
# if response.status_code == 200:
#     data = response.json()
#     print("Form submissions:", data)
# elif response.status_code == 401:
#     print("Unauthorized access. Check your authentication token.")
# elif response.status_code == 404:
#     print("Form not found.")
# else:
#     print("An error occurred:", response.text)
# Endpoint URL


#  REGISTER


# import requests
#
# url = 'http://localhost:8000/register'
#
# user_details = {
#     "name": "nev",
#     "email": "emejl",
#     "phone": "fon",
#     "pass": "passz",
#     "role": "rol"
# }
#
# response = requests.post(url, json=user_details)
#
# if response.status_code == 200:
#     token = response.json()["token"]
#     print("Registration successful. Token:", token)
# else:
#     print("Error:", response.status_code, response.json())


#   LOGIN


# import requests
#
# # Endpoint URL
# url = 'http://localhost:8000/login'
#
# # User details
# user_details = {
#     "email": "emejl",
#     "pass": "example_password"
# }
#
# # Make POST request
# response = requests.post(url, json=user_details)
#
# # Check response
# if response.status_code == 200:
#     token = response.json()["token"]
#     print("Login successful. Token:", token)
# elif response.status_code == 401:
#     print("Invalid username or password:", response.json()["detail"])
# else:
#     print("Error:", response.status_code, response.json())