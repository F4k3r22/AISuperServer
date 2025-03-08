from AISuperServer import SuperServerFlask
import random 
import string


def CreateDummyAPIKey():
    return f'dummy-apikey-{"".join(random.choices(string.ascii_uppercase + string.digits, k=64))}'

#api = CreateDummyAPIKey()
#print(api)

api_keys = ['dummy-apikey-OTXEYCZNS4NBR8YA9V0PBPV4VST2FBAE3PEZDKBDXKCQ88CSTIPI5NPOLN0ZN0CG', 'dummy-apikey-4VQF9L4NFF71GAW4NTOY6EPZUSE6SVNEKW3DHBHWGZIZM8IS8VTT2ZUR75Z0VBZI']

app = SuperServerFlask(
    model='llama3.2-vision',
    stream=True,
    multimodal=True,
    port=8080,
    api_key_required=True,
    api_keys=api_keys,
    enable_memory_monitor=True
)

print("Servidor ejecutándose en http://0.0.0.0:8080")