import pandas as pd
import numpy as np
import json

n_righe = 100000

np.random.seed(42)

ordini = pd.DataFrame({
  "ClienteID": np.random.randint(1, 5001, n_righe),
  "ProdottoID": np.random.randint(1,20, size=n_righe),
  "Quantità": np.random.randint(1, 3, size=n_righe ),
  "DataOrdine": np.random.choice(pd.date_range("2026-01-01", "2026-12-31", freq="D"), n_righe),
  "Prezzo": np.random.randint(50, 1000, n_righe)
})


prodotti = pd.json_normalize([
  {"Prodotto": "Laptop Pro X", "Fornitore": "Ruda"},
  {"Prodotto": "Cuffie Wireless Zeta", "Fornitore": "Pieris"},
  {"Prodotto": "Smartwatch Pulse 4", "Fornitore": "Ruda"},
  {"Prodotto": "Frullatore TurboMix", "Fornitore": "Napoli"},
  {"Prodotto": "Monitor UltraHD 27", "Fornitore": "Ruda"},
  {"Prodotto": "Sedia Ergonomica Flex", "Fornitore": "Pieris"},
  {"Prodotto": "Zaino Trekking 40L", "Fornitore": "Ruda"},
  {"Prodotto": "Lampada LED Smart", "Fornitore": "Pieris"},
  {"Prodotto": "Tastiera Meccanica RedSwitch", "Fornitore": "Ruda"},
  {"Prodotto": "Aspirapolvere Cyclone", "Fornitore": "Pieris"},
  {"Prodotto": "Action Cam 4K GoFast", "Fornitore": "Napoli"},
  {"Prodotto": "Set Pentole Acciaio", "Fornitore": "Pieris"},
  {"Prodotto": "Router WiFi AX3000", "Fornitore": "Ruda"},
  {"Prodotto": "Scarpe Running Aero", "Fornitore": "Pieris"},
  {"Prodotto": "Cassa Bluetooth Boom", "Fornitore": "Ruda"},
  {"Prodotto": "Tablet NovaTab 10", "Fornitore": "Isernia"},
  {"Prodotto": "Macchina Caffè MiniBar", "Fornitore": "Ruda"},
  {"Prodotto": "Ventilatore TurboFan", "Fornitore": "Pieris"},
  {"Prodotto": "Piastra Capelli SilkPro", "Fornitore": "Ruda"},
  {"Prodotto": "Powerbank 20000mAh", "Fornitore": "Pieris"}
])

prodotti["ProdottoID"] = np.arange(1, 21)


n_clienti = 5000
regione = ["FVG", "Campania", "Molise"]
segmento = ["Elegance", "Classic", "Hobby"]

clienti = pd.DataFrame({"Clienti": np.arange(1, n_clienti + 1), "Regione": np.random.choice(regione, n_clienti), "Segmento": np.random.choice(segmento, n_clienti)})

clienti["ClienteID"] = np.arange(1, 5001)

ordini.to_csv("ordini.csv", index=False)
prdini = pd.read_csv("ordini.csv")

prodotti.to_json("prodotti.json", orient="records")
prodotti = pd.read_json("prodotti.json")

clienti.to_csv("clienti.csv", index=False)
clienti = pd.read_csv("clienti.csv")

df_unificato = pd.merge(ordini, clienti, on="ClienteID", how="left")

df_finale = pd.merge(df_unificato, prodotti, on="ProdottoID", how="left")



df_finale[["ClienteID", "ProdottoID", "Quantità", "Clienti"]] = df_finale[["ClienteID", "ProdottoID", "Quantità", "Clienti"]].fillna(0).astype("int32")
df_finale[["Prezzo"]] = df_finale[["Prezzo"]].fillna(df_finale["Prezzo"].mean()).astype("float32")
df_finale[["Regione", "Segmento"]] = df_finale[["Regione", "Segmento"]].astype("category")

print(df_finale.info())

df_finale["Valore_totale"] = df_finale["Quantità"] * df_finale["Prezzo"]
print(df_finale)

df_finale_filtrato = df_finale[df_finale["Valore_totale"] > 100]


print(df_finale_filtrato)