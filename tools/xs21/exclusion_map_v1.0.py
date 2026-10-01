"""B7-Klassifikation v1.0 fuer XS21 PiT v1.0 (FREEZE-KANDIDAT), Stand 01.10.2026.

REGEL (M1, Wortlaut v1.0 §2.4): Zugelassen sind nur Perpetuals auf ein einzelnes Krypto-Asset, dessen oekonomisches Exposure
nicht an einen Fiat-Wert, einen Rohstoff, ein Wertpapier oder einen Index gebunden ist. Ausgeschlossen sind Stablecoins,
tokenisierte Rohstoffe und Wertpapiere sowie Index- und Korb-Perps.

AUFFANGREGEL (M2): Bleibt ein Symbol nach Pruefung der Binance-Ankuendigung unklar: Binance-Spot-Paar oder identifizierbarer
On-Chain-Token -> zugelassen (Kennzeichen 'auffang'); fehlt beides -> ausgeschlossen.

Grundlage NUR: Symbolnamen, Listing-Monate, Binance-Ankuendigungen (Feld Underlying / TradFi-Kennzeichnung), Binance-Spot-Listing.
Keine Kurse, Renditen oder Volumen. Alle nicht aufgefuehrten Symbole sind Einzel-Krypto-Assets nach Regel (Normalfall seit 2019).
Felder: typ, sicherheit (sicher | wahrscheinlich | auffang), grund, quelle (Pruefdatum 2026-10-01 fuer alle Eintraege)."""

ZULASSEN_TYP = {"KRYPTO_EINZEL"}

# Quellen (Binance-Ankuendigungen bzw. Nachrichten mit Wortlaut der Ankuendigung, abgerufen 2026-10-01)
Q = {
    "K": "Ticker-/Fondskenntnis (v0.1), Ankuendigung nicht einzeln abgerufen",
    "TF0702": "Binance TradFi-Listing 2026-07-02 (bbx.com/news-detail/2964654)",
    "TF0709": "Binance TradFi-Listing 2026-07-09 (gate.com/news/detail/...22463575)",
    "TF0721": "Binance-Ankuendigung TradFi 2026-07-21 (treeofalpha.com/preview_article?id=1784619910945)",
    "TF0817": "Binance TradFi-Listing 2026-08-17 (coin.t0ols.com/announcements/binance-2026-08-17-c0bc5c)",
    "TF0825": "Binance TradFi-Listing 2026-08-25 (cryptonews.net/news/market/33345244)",
    "TF0828": "Binance-Ankuendigung TradFi 2026-08-28 (treeofalpha.com/preview_article?id=1787902209365)",
    "TF0918": "Binance TradFi-Listing 2026-09-18 (bbx.com/news-detail/3088049)",
    "TF0929": "Binance TradFi-Listing 2026-09-29 (tokenpost.com/news/business/25184; coinrf Help Center)",
    "TF09XX": "Binance TradFi-Listing LLY/NVO/BBX/NOK/EWT/ASTS (bbx.com/news-detail/2911684)",
    "TFJAN": "Binance TradFi-Start 2026-01-05/07 XAU/XAG, TSLA 2026-01-28 (binance.info Ankuendigung)",
    "TFFEB": "Binance Academy: Equity-Perps Feb. 2026 MSTR/AMZN/CRCL/COIN/PLTR",
    "PAYP": "Binance-Ankuendigung Equity Perpetual PAYPUSDT 2026-03-23 (binance.info)",
    "CBRS": "Binance-Ankuendigung TradFi CBRSUSDT 2026-05-19 (Binance Square)",
    "STXX": "Binance TradFi-Listing 2026-06-11, Seagate (coinlive.com/news-flash/1115443)",
    "MOON": "Binance Pre-IPO-Perp MOONSHOTUSDT 2026-09-22 (theblockbeats.news/flash/368402)",
    "FRAX": "Binance: FXS->FRAX Swap 2026-01-15, FRAXUSDT-Perp 2026-01-15, Underlying Frax (FRAX) (treeofalpha id=1768462206116)",
    "STBL": "Binance Futures STBLUSDT 2025-09-17, Underlying STBL-Token (Plattform-/Governance-Token)",
    "STABLE": "Binance Pre-Market STABLEUSDT 2025-11-06, Underlying Stable (STABLE), Layer-1-Token (Binance Square)",
    "USTC": "first_month 2023-11 (binance_um_universe.csv) liegt nach der Entkopplung im Mai 2022",
    "SPOT": "Binance-Spot-USDT-Paar vorhanden (data.binance.vision Spot-Listing 2026-10-01), Ankuendigung nicht widersprechend",
}
def A(name, date): return f"Binance-Ankuendigung Perpetual {name} {date}, Underlying Krypto-Token"

E, F, C, X, P, S, T, I, K = "AKTIE", "ETF", "ROHSTOFF", "DEVISEN", "PRE_IPO", "STABLECOIN", "TOKENISIERTER_ROHSTOFF", "INDEX", "KRYPTO_EINZEL"
M = {}
def add(typ, conf, quelle, items):
    for k, v in items.items():
        assert k not in M, k
        M[k] = dict(typ=typ, sicherheit=conf, grund=v, quelle=Q.get(quelle, quelle))

# ---------------- Ausschluesse: Aktien
add(E, "sicher", "K", {
    "AAPL": "Apple Inc.", "ADBE": "Adobe Inc.", "AMAT": "Applied Materials", "AMD": "Advanced Micro Devices",
    "ARM": "Arm Holdings", "ASML": "ASML Holding", "AVGO": "Broadcom", "BABA": "Alibaba Group", "BMNR": "BitMine Immersion Technologies (Aktie)",
    "BRKB": "Berkshire Hathaway B", "CIEN": "Ciena", "COHR": "Coherent", "COST": "Costco", "CRDO": "Credo Technology", "CRM": "Salesforce",
    "CRWD": "CrowdStrike", "CRWV": "CoreWeave", "CSCO": "Cisco", "CVNA": "Carvana", "DDOG": "Datadog", "DELL": "Dell Technologies",
    "DIS": "Walt Disney", "DKNG": "DraftKings", "EBAY": "eBay", "FLNC": "Fluence Energy", "GEV": "GE Vernova", "GLW": "Corning", "GME": "GameStop",
    "GOOGL": "Alphabet A", "GPRO": "GoPro", "GS": "Goldman Sachs", "GTLB": "GitLab", "HD": "Home Depot", "HIMS": "Hims & Hers Health",
    "HK0700": "Tencent Holdings (HKEX 0700)", "HK1810": "Xiaomi (HKEX 1810)", "HK0992": "Lenovo Group (HKEX 0992)", "HOOD": "Robinhood Markets",
    "HPE": "Hewlett Packard Enterprise", "IBM": "IBM", "INTC": "Intel", "IREN": "IREN Ltd (Aktie)", "JPM": "JPMorgan Chase",
    "KLAC": "KLA Corp", "LITE": "Lumentum", "LRCX": "Lam Research", "MDB": "MongoDB", "META": "Meta Platforms", "MRVL": "Marvell Technology",
    "MSFT": "Microsoft", "MU": "Micron Technology", "NBIS": "Nebius Group", "NFLX": "Netflix", "NOW": "ServiceNow", "NVDA": "NVIDIA",
    "OKLO": "Oklo", "ORCL": "Oracle", "PYPL": "PayPal", "QCOM": "Qualcomm", "RDDT": "Reddit", "RIVN": "Rivian", "RKLB": "Rocket Lab",
    "SAMSUNG": "Samsung Electronics", "SKHYNIX": "SK hynix", "SMCI": "Super Micro Computer", "SNDK": "Sandisk", "SNOW": "Snowflake",
    "SONY": "Sony Group", "TEAM": "Atlassian", "TENCENT": "Tencent Holdings", "TSM": "Taiwan Semiconductor (ADR)", "UBER": "Uber Technologies",
    "WDC": "Western Digital", "WMT": "Walmart", "XOM": "Exxon Mobil", "ZM": "Zoom Communications", "ZS": "Zscaler",
})
add(E, "sicher", "TFJAN", {"TSLA": "Tesla"})
add(E, "sicher", "TFFEB", {"MSTR": "Strategy Inc. (Aktie)", "AMZN": "Amazon.com", "CRCL": "Circle Internet Group (Aktie)", "COIN": "Coinbase Global (Aktie)", "PLTR": "Palantir Technologies"})
add(E, "sicher", "TF0702", {"STRC": "Strategy Inc. Vorzugsaktie STRC", "CAT": "Caterpillar", "TXN": "Texas Instruments", "FLEX": "Flex Ltd", "TER": "Teradyne",
                            "TTWO": "Take-Two Interactive", "BSP": "Bending Spoons"})
add(E, "sicher", "TF0709", {"BOT": "RoboStrategy", "WEN": "Wendy's", "BNC": "CEA Industries", "FWDI": "Forward Industries"})
add(E, "sicher", "TF0721", {"SHAZ": "SharonAI Holdings", "SOFI": "SoFi Technologies", "PANW": "Palo Alto Networks", "PENG": "Penguin Solutions"})
add(E, "sicher", "TF0817", {"NET": "Cloudflare", "VST": "Vistra", "SHOP": "Shopify", "CXMT": "CXMT Corporation"})
add(E, "sicher", "TF0825", {"DJT": "Trump Media & Technology Group", "MRNA": "Moderna"})
add(E, "sicher", "TF0828", {"TEM": "Tempus AI", "MRK": "Merck & Co", "IONQ": "IonQ", "MARA": "MARA Holdings (Aktie)", "PDD": "PDD Holdings"})
add(E, "sicher", "TF0918", {"PATH": "UiPath", "AMC": "AMC Entertainment", "ANET": "Arista Networks", "HUT": "Hut 8 (Aktie)", "APLD": "Applied Digital",
                            "AGPU": "TradFi-Perp (Aktie)", "CYPH": "TradFi-Perp (Quelle nennt CYPUSDT)"})
add(E, "sicher", "TF0929", {"CRML": "Critical Metals", "ACN": "Accenture", "MP": "MP Materials", "SECZ": "TradFi-Perp", "UNH": "UnitedHealth Group", "NKE": "Nike"})
add(E, "sicher", "TF09XX", {"LLY": "Eli Lilly", "NVO": "Novo Nordisk", "BBX": "TradFi-Perp", "NOK": "Nokia", "ASTS": "AST SpaceMobile"})
add(E, "sicher", "PAYP", {"PAYP": "PayPay Corporation"})
add(E, "sicher", "CBRS", {"CBRS": "Cerebras Systems"})
add(E, "sicher", "STXX", {"STXX": "Seagate Technology (STX)"})
add(E, "wahrscheinlich", "K", {
    "AAOI": "Applied Optoelectronics", "ALAB": "Astera Labs", "APP": "AppLovin", "AXTI": "AXT Inc", "BE": "Bloom Energy", "BX": "Blackstone",
    "BYD": "BYD Company", "GIGADEV": "GigaDevice Semiconductor", "HANMI": "Hanmi Semiconductor", "HK0625": "HKEX-Code 0625",
    "HYUNDAI": "Hyundai Motor", "KO": "Coca-Cola", "KUAISHOU": "Kuaishou Technology", "LGELECTRONICS": "LG Electronics", "MEITUAN": "Meituan",
    "NAVER": "NAVER Corp", "ONDS": "Ondas Holdings", "POPMART": "Pop Mart International", "RUM": "Rumble", "SAMSUNGEM": "Samsung Electro-Mechanics",
    "SKHY": "SK hynix (zweite Notierung)", "TWST": "Twist Bioscience", "USAR": "USA Rare Earth", "V": "Visa", "VRT": "Vertiv", "ZHONGJI": "Zhongji Innolight",
})
# ---------------- ETFs
add(F, "sicher", "K", {
    "BITO": "ProShares Bitcoin Strategy ETF (Fondsanteil)", "EWJ": "iShares MSCI Japan", "EWY": "iShares MSCI South Korea", "EWZ": "iShares MSCI Brazil",
    "IWM": "iShares Russell 2000", "QQQ": "Invesco QQQ", "SMH": "VanEck Semiconductor", "SOXL": "Direxion Semiconductor Bull 3x",
    "SOXS": "Direxion Semiconductor Bear 3x", "SPY": "SPDR S&P 500", "SQQQ": "ProShares UltraPro Short QQQ", "TQQQ": "ProShares UltraPro QQQ",
    "TSLL": "Direxion Daily TSLA Bull 2x", "NVDL": "GraniteShares 2x Long NVDA", "UVXY": "ProShares Ultra VIX Short-Term", "XLE": "Energy Select Sector SPDR",
    "TBT": "ProShares UltraShort 20+ Year Treasury", "TMF": "Direxion 20+ Yr Treasury Bull 3x", "TZA": "Direxion Small Cap Bear 3x",
    "URNM": "Sprott Uranium Miners", "KODEX200": "Samsung KODEX 200", "CSOPSAMSUNG2L": "CSOP Samsung Electronics 2x", "CSOPSKHYNIX2L": "CSOP SK hynix 2x",
})
add(F, "sicher", "TF0702", {"KSTR": "Sci-Tech Innovation 50 ETF"})
add(F, "sicher", "TF0709", {"INTW": "GraniteShares 2x Long Intel", "SNXX": "Tradr 2x Long SanDisk", "XBI": "SPDR S&P Biotech"})
add(F, "sicher", "TF0817", {"GDX": "VanEck Gold Miners", "LYTE": "Roundhill Photonics & Optics"})
add(F, "sicher", "TF0825", {"SKUU": "GraniteShares 2x Long SK hynix", "SKDD": "GraniteShares 2x Short SK hynix", "RAM": "Roundhill T-REX 2x Long DRAM"})
add(F, "sicher", "TF0929", {"BWET": "Breakwave Tanker Shipping ETF"})
add(F, "sicher", "TF09XX", {"EWT": "iShares MSCI Taiwan"})
add(F, "wahrscheinlich", "K", {"KORU": "Direxion MSCI South Korea Bull 3x", "MUU": "Direxion Daily MU Bull 2x", "SLX": "VanEck Steel",
                               "DRAM": "Roundhill Memory ETF", "MVLL": "2x MRVL", "QNTX": "2x Hebel-ETF"})
# ---------------- Rohstoffe, Devisen, Pre-IPO, Stablecoins, tokenisierte Rohstoffe, Indizes
add(C, "sicher", "TFJAN", {"XAU": "Gold", "XAG": "Silber"})
add(C, "sicher", "K", {"XPT": "Platin", "XPD": "Palladium", "CL": "WTI-Rohoel", "NATGAS": "Erdgas", "COPPER": "Kupfer"})
add(C, "wahrscheinlich", "K", {"BZ": "Brent-Rohoel"})
add(X, "sicher", "K", {"USDBRL": "Devisenkurs USD/BRL"})
add(P, "sicher", "MOON", {"MOONSHOT": "Moonshot AI (Pre-IPO-Perp)"})
add(P, "wahrscheinlich", "K", {"ANTHROPIC": "Anthropic", "OPENAI": "OpenAI", "SPCX": "SpaceX", "UNITREE": "Unitree Robotics", "MINIMAX": "MiniMax",
                               "ZHIPU": "Zhipu AI", "OURA": "Oura Health"})
add(S, "sicher", "K", {"USDC": "USD Coin, an USD gebunden"})
add(T, "sicher", "K", {"PAXG": "PAX Gold, oekonomisch Gold", "XAUT": "Tether Gold, oekonomisch Gold"})
add(I, "sicher", "K", {"BTCDOM": "BTC-Dominanz-Index (Spread BTC gegen Altcoin-Korb)", "DEFI": "Binance-DeFi-Index (Korb)",
                       "FOOTBALL": "Fan-Token-Index (Korb)", "BLUEBIRD": "Index (Korb)"})

# ---------------- Zulassungen mit Pruefung (Regel erfuellt)
add(K, "sicher", "USTC", {"USTC": "TerraClassicUSD: Listing nach Entkopplung, nie als gebundener Stablecoin gehandelt"})
add(K, "sicher", "FRAX", {"FRAX": "Frax-Token nach Umbenennung von FXS, kein Stablecoin"})
add(K, "sicher", "STBL", {"STBL": "STBL-Plattform-Token (nicht der Stablecoin USST)"})
add(K, "sicher", "STABLE", {"STABLE": "Layer-1-Token der Stable-Chain"})
for sym, (name, date) in {
    "ACU": ("ACUUSDT (Acurast)", "2026-01-21"), "ARX": ("ARXUSDT (Arcium)", "2026-06-23"), "BASED": ("BASEDUSDT (Based)", "2026-03-30"),
    "BSB": ("BSBUSDT (Block Street)", "2026-03-25"), "BILL": ("BILLUSDT (Billions Network)", "2026-05-07"), "BTW": ("BTWUSDT (Bitway)", "2026-06-04"),
    "ZEST": ("ZESTUSDT (Zest Protocol)", "2026-06-04"), "CTR": ("CTRUSDT (Citrea)", "2026-05-28"), "DATAIP": ("DATAIPUSDT (Data Network)", "2026-07-03"),
    "DOS": ("DOSUSDT (DAPPOS)", "2026-08-12"), "STAR": ("STARUSDT (Starpower)", "2026-05-14"), "PRL": ("PRLUSDT (Perle)", "2026-04-01"),
    "US": ("USUSDT (Talus Network)", "2025-12-12"), "CYS": ("CYSUSDT (Cysic)", "2025-12-12"), "GUA": ("GUAUSDT", "2025-12-21"), "IR": ("IRUSDT", "2025-12-21"),
    "COLLECT": ("COLLECTUSDT", "2025-12-31"), "MAGMA": ("MAGMAUSDT", "2025-12-31"), "EDGE": ("EDGEUSDT (edgeX)", "2026-03-19"),
    "GWEI": ("GWEIUSDT (ETHGas)", "2026-01-29"), "INX": ("INXUSDT (Infinex)", "2026-01-30"), "POWER": ("POWERUSDT", "2025-12-06"),
    "RLS": ("RLSUSDT", "2025-12-02"), "WET": ("WETUSDT", "2025-12-10"), "RAVE": ("RAVEUSDT", "2025-12-14"), "SKR": ("SKRUSDT (Solana Mobile Seeker)", "2026-01-22"),
    "SPORTFUN": ("SPORTFUNUSDT (Sport.Fun)", "2026-01-16"), "SPACE": ("SPACEUSDT", "2026-01-23"), "TRIA": ("TRIAUSDT (Tria)", "2026-02-06"),
    "CAP": ("CAPUSDT (Cap)", "2026-06-27"),
}.items():
    add(K, "sicher", A(name, date), {sym: "Krypto-Token laut Ankuendigung (Standard-Perpetual, nicht TradFi)"})
add(K, "wahrscheinlich", A("PONSUSDT", "2026-09-06"), {"PONS": "Standard-Perpetual zusammen mit Meme-Token gelistet, Underlying im Auszug nicht genannt"})
add(K, "wahrscheinlich", "Binance Futures OUSDT 2026-06-24 (gate.com/news/detail/...22078664)", {"O": "Token des O1-Exchange-Oekosystems; Bezug zu Stablecoin-Wrapper, Peg nicht belegt"})
for s in ["CHIP", "GENIUS", "GRAM", "KAT", "MARSCOIN", "OPG", "OPN", "RE", "ROBO"]:
    add(K, "auffang", "SPOT", {s: "Auffangregel M2: Spot-Paar vorhanden"})
