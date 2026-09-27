import feedparser
import json
import os
from datetime import datetime

# ============================================
# FONTES DE NOTÍCIAS (feeds RSS)
# Adicione ou remova links quando quiser
# ============================================
FONTES = [
    {"nome": "Roblox - Anúncios", "url": "https://devforum.roblox.com/c/updates/announcements/36.rss"},
    {"nome": "Roblox - Atualizações", "url": "https://devforum.roblox.com/c/updates/release-notes/62.rss"},
    {"nome": "IGN Brasil", "url": "https://br.ign.com/feed.xml"},
    {"nome": "Steam News", "url": "https://store.steampowered.com/feeds/news.xml"},
    {"nome": "PlayStation Blog", "url": "https://blog.playstation.com/feed/"},
    {"nome": "Xbox Wire", "url": "https://news.xbox.com/en-us/feed/"},
    {"nome": "Nintendo Life", "url": "https://www.nintendolife.com/feeds/news"},
    {"nome": "GameSpot", "url": "https://www.gamespot.com/feeds/news/"},
]

MAX_POR_FONTE = 10   # Quantas notícias pegar de cada fonte

noticias = []
print("🤖 Robô iniciado. Coletando notícias...")

for fonte in FONTES:
    try:
        print(f"→ Lendo: {fonte['nome']}")
        feed = feedparser.parse(fonte["url"])

        for item in feed.entries[:MAX_POR_FONTE]:
            # Pega a imagem (se existir no feed)
            imagem = ""
            if hasattr(item, "media_content") and item.media_content:
                imagem = item.media_content[0].get("url", "")
            elif hasattr(item, "enclosures") and item.enclosures:
                imagem = item.enclosures[0].get("href", "")

            noticias.append({
                "titulo": item.get("title", "Sem título"),
                "link": item.get("link", "#"),
                "resumo": item.get("summary", "")[:300],
                "fonte": fonte["nome"],
                "data": item.get("published", ""),
                "imagem": imagem,
            })
    except Exception as e:
        print(f"❌ Erro na fonte {fonte['nome']}: {e}")

# Ordena por data (mais recentes primeiro)
noticias.sort(key=lambda x: x.get("data", ""), reverse=True)

# Remove duplicadas (mesmo link)
vistos = set()
unicas = []
for n in noticias:
    if n["link"] not in vistos:
        vistos.add(n["link"])
        unicas.append(n)

# Garante que a pasta data/ existe
os.makedirs("data", exist_ok=True)

with open("data/noticias.json", "w", encoding="utf-8") as f:
    json.dump({
        "atualizado_em": datetime.now().strftime("%d/%m/%Y às %H:%M"),
        "total": len(unicas),
        "noticias": unicas,
    }, f, ensure_ascii=False, indent=2)

print(f"✅ Pronto! {len(unicas)} notícias salvas em data/noticias.json")
