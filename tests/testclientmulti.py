from AISuperServer import SuperServerClient
from pathlib import Path

dummy_api_key = 'dummy-apikey-OTXEYCZNS4NBR8YA9V0PBPV4VST2FBAE3PEZDKBDXKCQ88CSTIPI5NPOLN0ZN0CG'

client = SuperServerClient(api_key=dummy_api_key, multimodal=True)

image_path = Path("Logo.png").resolve()

image_path = str(image_path)

print(image_path)

query = client.Query('Oye describe la imagen y dime que hay de llamativo y de que producto puede ser la imagen', image_path=image_path, stream=True)

# Toma en cuenta que si tu servidor es levantado en un host y puerto diferente al '0.0.0.0:8080'
# Debes configuraro en el SuperServerClient algo asi: SuperServerClient(host='Tu host', port= 'Tu puerto')
# Y se ha configurado al api_key porque el servidor que levantamos para probar el cliente lo configuramos con api_key