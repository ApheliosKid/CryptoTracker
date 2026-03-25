import requests

def ia_pret_crypto(nume_moneda):

    api_key = f"https://api.coingecko.com/api/v3/simple/price?ids={nume_moneda}&vs_currencies=usd"

    raspuns  = requests.get(api_key)

    if raspuns.status_code == 200:

        dictionar = raspuns.json()

        if nume_moneda in dictionar:
            pret = dictionar[nume_moneda]["usd"]
            return pret
        else:
            return None

    else:
        print(f"Eroare, sv nu a raspuns : {raspuns.status_code}")
        return None
