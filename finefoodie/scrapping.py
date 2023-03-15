import requests
res = requests.get("https://www.tripadvisor.in/Restaurant_Review-g297635-d1205738-Reviews-Hotel_Paragon_Restaurant-Kozhikode_Kozhikode_District_Kerala.html")
print(res.text)