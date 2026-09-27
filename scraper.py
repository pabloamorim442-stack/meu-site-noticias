import feedparser
import json
import os
from datetime import datetime

# ============================================
# FONTES DE NOTÍCIAS (com CATEGORIA)
# ============================================
FONTES = [
    {"nome": "Roblox - Anúncios", "url": "https://devforum.roblox.com/c/updates/announcements/36.rss", "categoria": "Roblox"},
    {"nome": "Roblox - Atualizações", "url": "https://devforum.roblox.com/c/updates/release-notes/62.rss", "categoria": "Roblox"},
    {"nome": "IGN Brasil", "url": "https://br.ign.com/feed.xml", "categoria": "Geral"},
    {"nome": "Steam News", "url": "https://store.steampowered.com/feeds/news.xml", "categoria": "Steam"},
    {"nome": "PlayStation Blog", "url": "https://blog.playstation.com/feed/", "categoria": "PlayStation"},
    {"nome": "Xbox Wire", "url": "https://news.xbox.com/en-us/feed/", "categoria": "Xbox"},
    {"nome": "Nintendo Life", "url": "https://www.nintendolife.com/feeds/news", "categoria": "Nintendo"},
    {"nome": "GameSpot", "url": "https://www.gamespot.com/feeds/news/", "categoria": "Geral"},
]

MAX_POR_FONTE = 10
ARQUIVO_JA_POSTADO = "data/postados.json"   # Guarda links já postados no Bluesky

noticias = []
print("🤖 Robô iniciado. Coletando notícias...")

for fonte in FONTES:
    try:
        print(f"→ Lendo: {fonte['nome']}")
        feed = feedparser.parse(fonte["url"])

        for item in feed.entries[:MAX_POR_FONTE]:
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
                "categoria": fonte["categoria"],
                "data": item.get("published", ""),
                "imagem": imagem,
            })
    except Exception as e:
        print(f"❌ Erro na fonte {fonte['nome']}: {e}")

# Ordena e remove duplicadas
noticias.sort(key=lambda x: x.get("data", ""), reverse=True)
vistos = set()
unicas = []
for n in noticias:
    if n["link"] not in vistos:
        vistos.add(n["link"])
        unicas.append(n)

os.makedirs("data", exist_ok=True)

with open("data/noticias.json", "w", encoding="utf-8") as f:
    json.dump({
        "atualizado_em": datetime.now().strftime("%d/%m/%Y às %H:%M"),
        "total": len(unicas),
        "noticias": unicas,
    }, f, ensure_ascii=False, indent=2)

print(f"✅ {len(unicas)} notícias salvas em data/noticias.json")


# ============================================
# POSTAR NO BLUESKY (notícias novas)
# ============================================
def postar_bluesky():
    handle = os.environ.get("BLUESKY_HANDLE")
    senha = os.environ.get("BLUESKY_PASSWORD")

    if not handle or not senha:
        print("⚠️ Bluesky não configurado. Pulando esta etapa.")
        return

    try:
        from atproto import Client
    except ImportError:
        print("⚠️ Biblioteca atproto não instalada. Pulando.")
        return

    # Carrega links já postados
    ja_postados = []
    if os.path.exists(ARQUIVO_JA_POSTADO):
        with open(ARQUIVO_JA_POSTADO, "r", encoding="utf-8") as f:
            ja_postados = json.load(f)

    # Filtra notícias novas (ainda não postadas)
    novas = [n for n in unicas if n["link"] not in ja_postados]

    if not novas:
        print("👍 Nada novo para postar no Bluesky.")
        return

    # Limita a 5 posts por execução (pra não floodar)
    novas = novas[:5]

    client = Client()
    client.login(handle, senha)
    print(f"🐦 Conectado ao Bluesky como {handle}")

    for n in novas:
        texto = f"🎮 {n['titulo']}\n\n📌 {n['categoria']} • {n['fonte']}\n\n{n['link']}"

        # Bluesky tem limite de 300 caracteres
        if len(texto) > 300:
            texto = texto[:295] + "..."

        try:
            client.send_post(texto)
            print(f"   ✅ Postado: {n['titulo'][:60]}...")
            ja_postados.append(n["link"])
        except Exception as e:
            print(f"   ❌ Erro ao postar '{n['titulo'][:40]}': {e}")

    # Salva a lista atualizada
    with open(ARQUIVO_JA_POSTADO, "w", encoding="utf-8") as f:
        json.dump(ja_postados, f, ensure_ascii=False, indent=2)

    print(f"✅ Bluesky: {len(novas)} notícias postadas.")


postar_bluesky()
