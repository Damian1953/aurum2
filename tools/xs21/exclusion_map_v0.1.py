"""Manuelle Klassifikation nach BASISWERT (nicht nach Ergebnis) fuer B7, Stand 01.10.2026. ENTWURF.
Quelle der Einordnung: allgemein bekannte Boersenticker/Fonds/Rohstoffcodes und Binance-Ankuendigungen zu TradFi-Perps
(ab 2026-01-05: XAUUSDT, XAGUSDT, TSLAUSDT, MSTR/AMZN/CRCL/COIN/PLTR, ETFs, Oel, Erdgas). Es wurden KEINE Kurse, Renditen
oder Volumen betrachtet. sicher = eindeutiger Ticker; wahrscheinlich = plausibel, vor dem Freeze gegen die
Binance-Ankuendigung pruefen. UNKLAR = Basiswert nicht eindeutig bestimmbar, vorlaeufig NICHT ausgeschlossen, vor Freeze klaeren."""

E, F, C, X, P, S, T = "EQUITY", "ETF", "COMMODITY", "FX", "PRE_IPO", "STABLECOIN", "TOKENIZED_COMMODITY"

def _m(cat, conf, items):
    return {k: (cat, conf, v) for k, v in items.items()}

EXCL = {}
EXCL.update(_m(E, "sicher", {
    "AAPL": "Apple Inc.", "ADBE": "Adobe Inc.", "AMAT": "Applied Materials", "AMD": "Advanced Micro Devices", "AMZN": "Amazon.com",
    "ANET": "Arista Networks", "APP": "AppLovin", "ARM": "Arm Holdings", "ASML": "ASML Holding", "ASTS": "AST SpaceMobile",
    "AVGO": "Broadcom", "BABA": "Alibaba Group", "BMNR": "BitMine Immersion Technologies (Aktie, nicht ETH)", "BRKB": "Berkshire Hathaway B",
    "CIEN": "Ciena", "COHR": "Coherent", "COIN": "Coinbase Global (Aktie)", "COST": "Costco", "CRCL": "Circle Internet Group (Aktie)",
    "CRDO": "Credo Technology", "CRM": "Salesforce", "CRWD": "CrowdStrike", "CRWV": "CoreWeave", "CSCO": "Cisco", "CVNA": "Carvana",
    "DDOG": "Datadog", "DELL": "Dell Technologies", "DIS": "Walt Disney", "DJT": "Trump Media & Technology Group", "DKNG": "DraftKings",
    "EBAY": "eBay", "FLNC": "Fluence Energy", "GEV": "GE Vernova", "GLW": "Corning", "GME": "GameStop", "GOOGL": "Alphabet A",
    "GPRO": "GoPro", "GS": "Goldman Sachs", "GTLB": "GitLab", "HD": "Home Depot", "HIMS": "Hims & Hers Health",
    "HK0700": "Tencent Holdings (HKEX 0700)", "HK1810": "Xiaomi (HKEX 1810)", "HK0992": "Lenovo Group (HKEX 0992)",
    "HOOD": "Robinhood Markets", "HPE": "Hewlett Packard Enterprise", "HUT": "Hut 8 (Aktie)", "IBM": "IBM", "INTC": "Intel",
    "IONQ": "IonQ", "IREN": "IREN Ltd (Aktie)", "JPM": "JPMorgan Chase", "KLAC": "KLA Corp", "LITE": "Lumentum", "LLY": "Eli Lilly",
    "LRCX": "Lam Research", "MARA": "MARA Holdings (Aktie)", "MDB": "MongoDB", "META": "Meta Platforms", "MRK": "Merck & Co",
    "MRNA": "Moderna", "MRVL": "Marvell Technology", "MSFT": "Microsoft", "MSTR": "Strategy Inc. (Aktie)", "MU": "Micron Technology",
    "NBIS": "Nebius Group", "NET": "Cloudflare", "NFLX": "Netflix", "NKE": "Nike", "NOK": "Nokia", "NOW": "ServiceNow", "NVDA": "NVIDIA",
    "NVO": "Novo Nordisk", "OKLO": "Oklo", "ORCL": "Oracle", "PANW": "Palo Alto Networks", "PATH": "UiPath", "PDD": "PDD Holdings",
    "PLTR": "Palantir Technologies", "PYPL": "PayPal", "QCOM": "Qualcomm", "RDDT": "Reddit", "RIVN": "Rivian", "RKLB": "Rocket Lab",
    "SAMSUNG": "Samsung Electronics", "SHOP": "Shopify", "SKHYNIX": "SK hynix", "SMCI": "Super Micro Computer", "SNDK": "Sandisk",
    "SNOW": "Snowflake", "SOFI": "SoFi Technologies", "SONY": "Sony Group", "STRC": "Strategy Inc. Vorzugsaktie STRC",
    "TEAM": "Atlassian", "TENCENT": "Tencent Holdings", "TSLA": "Tesla", "TSM": "Taiwan Semiconductor (ADR)", "TTWO": "Take-Two Interactive",
    "TXN": "Texas Instruments", "UBER": "Uber Technologies", "UNH": "UnitedHealth Group", "WDC": "Western Digital", "WMT": "Walmart",
    "XOM": "Exxon Mobil", "ZM": "Zoom Communications", "ZS": "Zscaler",
}))
EXCL.update(_m(E, "wahrscheinlich", {
    "AAOI": "Applied Optoelectronics", "ACN": "Accenture", "ALAB": "Astera Labs", "AMC": "AMC Entertainment", "APLD": "Applied Digital",
    "AXTI": "AXT Inc", "BE": "Bloom Energy", "BX": "Blackstone", "BYD": "BYD Company", "CAT": "Caterpillar (nicht 1000CAT/Simon's Cat)",
    "CRML": "Critical Metals", "FLEX": "Flex Ltd", "FWDI": "Forward Industries", "GIGADEV": "GigaDevice Semiconductor",
    "HANMI": "Hanmi Semiconductor", "HK0625": "Chongqing Changan Automobile? (HKEX-Code 0625, pruefen)", "HYUNDAI": "Hyundai Motor",
    "KO": "Coca-Cola", "KUAISHOU": "Kuaishou Technology", "LGELECTRONICS": "LG Electronics", "MEITUAN": "Meituan", "MP": "MP Materials",
    "NAVER": "NAVER Corp", "ONDS": "Ondas Holdings", "POPMART": "Pop Mart International", "RUM": "Rumble", "SAMSUNGEM": "Samsung Electro-Mechanics",
    "SKHY": "SK hynix (zweite Notierung, pruefen)", "TEM": "Tempus AI", "TER": "Teradyne", "TWST": "Twist Bioscience", "USAR": "USA Rare Earth",
    "V": "Visa", "VRT": "Vertiv", "VST": "Vistra", "ZHONGJI": "Zhongji Innolight", "BNC": "CEA Industries (Ticker BNC, pruefen)",
}))
EXCL.update(_m(F, "sicher", {
    "BITO": "ProShares Bitcoin Strategy ETF (Fondsanteil, nicht BTC)", "EWJ": "iShares MSCI Japan ETF", "EWT": "iShares MSCI Taiwan ETF",
    "EWY": "iShares MSCI South Korea ETF", "EWZ": "iShares MSCI Brazil ETF", "GDX": "VanEck Gold Miners ETF", "IWM": "iShares Russell 2000 ETF",
    "QQQ": "Invesco QQQ Trust", "SMH": "VanEck Semiconductor ETF", "SOXL": "Direxion Semiconductor Bull 3x", "SOXS": "Direxion Semiconductor Bear 3x",
    "SPY": "SPDR S&P 500 ETF", "SQQQ": "ProShares UltraPro Short QQQ", "TQQQ": "ProShares UltraPro QQQ", "TSLL": "Direxion Daily TSLA Bull 2x",
    "NVDL": "GraniteShares 2x Long NVDA", "UVXY": "ProShares Ultra VIX Short-Term Futures", "XBI": "SPDR S&P Biotech ETF",
    "XLE": "Energy Select Sector SPDR", "TBT": "ProShares UltraShort 20+ Year Treasury", "TMF": "Direxion Daily 20+ Yr Treasury Bull 3x",
    "TZA": "Direxion Daily Small Cap Bear 3x", "URNM": "Sprott Uranium Miners ETF", "KODEX200": "Samsung KODEX 200 ETF",
    "CSOPSAMSUNG2L": "CSOP Samsung Electronics Daily 2x Leveraged", "CSOPSKHYNIX2L": "CSOP SK hynix Daily 2x Leveraged",
}))
EXCL.update(_m(F, "wahrscheinlich", {
    "KORU": "Direxion MSCI South Korea Bull 3x", "MUU": "Direxion Daily MU Bull 2x", "SLX": "VanEck Steel ETF",
    "BWET": "Breakwave Tanker Shipping ETF", "DRAM": "Speicherchip-ETF (pruefen)", "SKUU": "2x SK hynix ETF (pruefen)",
    "SNXX": "2x SNOW ETF (pruefen)", "MVLL": "2x MRVL ETF (pruefen)", "QNTX": "2x Hebel-ETF (pruefen)",
}))
EXCL.update(_m(C, "sicher", {
    "XAU": "Gold", "XAG": "Silber", "XPT": "Platin", "XPD": "Palladium", "CL": "WTI-Rohoel", "NATGAS": "Erdgas", "COPPER": "Kupfer",
}))
EXCL.update(_m(C, "wahrscheinlich", {"BZ": "Brent-Rohoel (Kontraktcode BZ)"}))
EXCL.update(_m(X, "sicher", {"USDBRL": "Devisenkurs USD/BRL"}))
EXCL.update(_m(P, "wahrscheinlich", {
    "ANTHROPIC": "Anthropic (nicht boersenkotiert)", "OPENAI": "OpenAI (nicht boersenkotiert)", "SPCX": "SpaceX (nicht boersenkotiert)",
    "CXMT": "ChangXin Memory (nicht boersenkotiert)", "UNITREE": "Unitree Robotics", "MINIMAX": "MiniMax (KI-Unternehmen)",
    "ZHIPU": "Zhipu AI (KI-Unternehmen)", "OURA": "Oura Health (nicht boersenkotiert)",
}))
EXCL.update(_m(S, "sicher", {"USDC": "USD Coin, Stablecoin gegen USDT"}))
EXCL.update(_m(T, "zur_entscheidung", {
    "PAXG": "PAX Gold: Krypto-Token, Basiswert physisches Gold. Nach B7-Wortlaut (Basiswert Krypto-Asset) auszuschliessen, Entscheid Claude/Damian",
    "XAUT": "Tether Gold: Krypto-Token, Basiswert physisches Gold. Wie PAXG",
}))

# Bewusst NICHT ausgeschlossen (Basiswert Krypto), aber mit Vermerk:
KEEP_NOTE = {
    "BTCDOM": "Index der BTC-Dominanz (Krypto-Index)", "DEFI": "Binance-DeFi-Index (Korb aus Krypto-Token)",
    "FOOTBALL": "Fan-Token-Index (Krypto-Token)", "BLUEBIRD": "Krypto-Index", "USTC": "TerraClassicUSD, seit 2022 entkoppelter ehemaliger Stablecoin, verhaelt sich wie ein Krypto-Token (Entscheid Claude/Damian)",
    "FRAX": "Frax-Governance-Token (vormals FXS), kein Stablecoin (pruefen)", "STABLE": "Token der Stable-Chain, kein Stablecoin", "STBL": "STBL-Governance-Token, kein Stablecoin (pruefen)",
}

# Basiswert nicht eindeutig, vorlaeufig NICHT ausgeschlossen, vor Freeze gegen Binance-Ankuendigungen klaeren:
UNKLAR = ["ACU", "AGPU", "ARX", "BASED", "BBX", "BILL", "BOT", "BSB", "BSP", "BTW", "CAP", "CBRS", "CHIP", "COLLECT", "CTR", "CYPH",
          "DATAIP", "DOS", "GENIUS", "GRAM", "GUA", "GWEI", "INTW", "INX", "IR", "KSTR", "LYTE", "MARSCOIN", "MOONSHOT", "O", "OPG",
          "OPN", "PAYP", "PENG", "PONS", "POWER", "PRL", "RAM", "RE", "ROBO", "SECZ", "SHAZ", "SKDD", "SPACE", "STAR", "STXX", "US",
          "WEN", "ZEST", "EDGE", "KAT", "MAGMA", "RAVE", "RLS", "SKR", "SPORTFUN", "TRIA", "WET", "CYS"]
