import requests

URL = "https://petstore.swagger.io/v2/pet"

new_pet = {
    "name": "new dog 1",
    "photoUrls": [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFRmWtO1zrO6tt35ewAJOE9NpAb8yiwhbrBWyxjVQCZw&s"
  ]
}

# POST/PUT
response_post = requests.post(url=URL, json=new_pet)

if response_post.status_code == 200:
    print(response_post.json())
else:
    print("Error")


# DELETE
response_delete = requests.delete(url=URL+"1")

if response_delete.status_code == 204:
  print("Pet deleted!")
else:
  print("Error")