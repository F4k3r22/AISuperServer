from AISuperServer import SuperServerClient

dummy_api_key = 'dummy-apikey-OTXEYCZNS4NBR8YA9V0PBPV4VST2FBAE3PEZDKBDXKCQ88CSTIPI5NPOLN0ZN0CG'

client = SuperServerClient(api_key=dummy_api_key)
# Toma en cuenta que si tu servidor es levantado en un host y puerto diferente al '0.0.0.0:8080'
# Debes configuraro en el SuperServerClient algo asi: SuperServerClient(host='Tu host', port= 'Tu puerto')
# Y se ha configurado al api_key porque el servidor que levantamos para probar el cliente lo configuramos con api_key
query = client.Query('Oye explicame la secuencia de Fibonacci, como si se lo explicara a un niño pequeño', stream=True)