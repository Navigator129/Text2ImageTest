import requests

url = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-YGi1QDMf6n1Ptr1pxMZHsYpE/user-AcpRpsr51vN2FMAtL2TaqkiM/img-4gjVKz0p76XGQfy9XOTstqoV.png?st=2024-10-25T08%3A11%3A47Z&se=2024-10-25T10%3A11%3A47Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-10-24T20%3A11%3A36Z&ske=2024-10-25T20%3A11%3A36Z&sks=b&skv=2024-08-04&sig=gs6k8PX0V2m4HIsoQvq55jbQr8Glkp/NfPyRQ43JpMg%3D'
img = requests.get(url)
with open('img.png', 'wb') as f:
    f.write(img.content)

