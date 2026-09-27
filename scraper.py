import feedparser
import json
import os
from datetime import datetime

# ============================================
# LISTA DE FONTES (feeds RSS)
# Adicione ou remova links aqui quando quiser
# ============================================
FONTES = [
    # Roblox - Anúncios oficiais
    {"nome": "Roblox - Anúncios", "url": "https://devforum.roblox.com/c/updates/announcements/36.rss"},
    # Roblox - Notas de atualização
    {"nome": "Roblox - Atualizações", "url": "https://devforum.roblox.com/c/updates/release-notes/62.rss"},
    # Notícias gerais de games
    {"nome": "IGN Brasil", "url": "https://br.ign.com/feed.xml"},
    {"nome": "Steam News", "url": "https://store.steampowered.com/feeds/news.xml"},
    FONTES = [
    {"nome": "Roblox - Anúncios", "url": "https://devforum.roblox.com/c/updates/announcements/36.rss"},
    {"nome": "Roblox - Atualizações", "url": "https://devforum.roblox.com/c/updates/release-notes/62.rss"},
    {"nome": "IGN Brasil", "url": "https://br.ign.com/feed.xml"},
    {"nome": "Steam News", "url": "https://store.steampowered.com/feeds/news.xml"},
    # ADICIONE NOVOS ABAIXO:
    {"nome": "Minecraft", "url": "https://www.minecraft.net/en-us/feeds/community-content/rss"},
    {"nome": "PlayStation Blog", "url": "https://blog.playstation.com/feed/"},
    {"nome": "Xbox Wire", "url": "https://news.xbox.com/en-us/feed/"},
    {"nome": "Nintendo Life", "url": "https://www.nintendolife.com/feeds/news"},
    {"nome": "GameSpot", "url": "https://www.gamespot.com/feeds/news/"},
]

]

MAX_POR_FONTE = 5   # Quantas notícias pegar de cada fonte
noticias = []

print("🤖 Robô iniciado. Coletando notícias...")

for fonte in FONTES:
    try:
        print(f"→ Lendo: {fonte['nome']}")
        feed = feedparser.parse(fonte["url"])

        for item in feed.entries[:MAX_POR_FONTE]:
            noticias.append({
                "titulo": item.get("title", "Sem título"),
                "link": item.get("link", "#"),
                "resumo": item.get("summary", "")[:300],  # corta resumos gigantes
                "fonte": fonte["nome"],
                "data": item.get("published", str(datetime.now())),
            })
    except Exception as e:
        print(f"❌ Erro na fonte {fonte['nome']}: {e}")

# Ordena por data (mais recente primeiro, quando possível)
noticias.sort(key=lambda x: x["data"], reverse=True)

# Garante que a pasta data/ existe
os.makedirs("data", exist_ok=True)

with open("data/noticias.json", "w", encoding="utf-8") as f:
    json.dump({
        "atualizado_em": datetime.now().strftime("%d/%m/%Y às %H:%M"),
        "total": len(noticias),
        "noticias": noticias,
    }, f, ensure_ascii=False, indent=2)

print(f"✅ Pronto! {len(noticias)} notícias salvas em data/noticias.json")
