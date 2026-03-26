import discord
from api_manager import ia_pret_crypto
from manager_db import DatabaseManager
import asyncio

db = DatabaseManager()

print("Starting the bot...")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Succesfully connected as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_chat = message.content.lower()
    if message_chat.startswith('!price'):
        cuvinte = message_chat.split()
        if len(cuvinte) > 1:
            moneda = cuvinte[1]

            async with message.channel.typing():
                pret = ia_pret_crypto(moneda)
                if pret is not None:
                    await message.channel.send(f'📈 Hi, {message.author.name}! The current price for **{moneda.capitalize()}** is **${pret}**.')
                else:
                    await message.channel.send(f'❌ Could not find coin "{moneda}". Please make sure the name is correct.')

    elif message_chat == '!commands' or message_chat == '!helpcrypto':
        embed = discord.Embed(title="CryptoTracker Command Menu",
                              description="Hello! Here is the list of commands you can use:",
                              color=discord.Color.blue())
        embed.add_field(name="📈 !pret [coin_name]", value="Get real-time price (e.g., `!pret solana`)", inline=False)
        embed.add_field(name="🛒 !buy [coin] [amount]", value="Virtually add a coin to your vault",inline=False)
        embed.add_field(name="💼 !portfolio", value="View your investment value",inline=False)
        await message.channel.send(embed=embed)
    elif message_chat.startswith('!buy '):
        cuvinte = message_chat.split()

        if len(cuvinte) == 3:
            moneda = cuvinte[1]
            try:
                cantitate = float(cuvinte[2])

                async with message.channel.typing():
                    pret = ia_pret_crypto(moneda)
                    if pret is not None:
                        total_plata = pret * cantitate
                        db.adauga_in_portofoliu(moneda, pret, cantitate)

                        await message.channel.send(f'✅ Success! You "bought" **{cantitate} {moneda.capitalize()}** at **${pret}**.\n💰 Total invested: **${total_plata:.2f}**.')
                    else:
                        await message.channel.send(f'❌ Coin "{moneda}" not found.')
            except ValueError:
                await message.channel.send('❌ Please enter a valid amount (e.g., `!buy solana 2.5`).')
    elif message_chat == '!portfolio':
        async with message.channel.typing():
            date_salvate = db.citeste_portofoliu()

            if len(date_salvate) == 0:
                await message.channel.send("🕸️ Your portfolio is empty. Use `!buy` to add some coins!")
            else:
                embed_portofoliu = discord.Embed(title="💼 Your Crypto Portfolio",
                                                 color=discord.Color.green())
                valoare_totala_investita = 0
                valoare_totala_curenta = 0

                for rand in date_salvate:
                    nume = rand[0]
                    pret_achizitie = rand[1]
                    cantitate = rand[2]
                    pret_live = ia_pret_crypto(nume.lower())
                    if pret_live is None:
                        pret_live = pret_achizitie

                    valoare_investita = pret_achizitie * cantitate
                    valoare_curenta = pret_live * cantitate
                    profit_pierdere = valoare_curenta - valoare_investita

                    valoare_totala_investita += valoare_investita
                    valoare_totala_curenta += valoare_curenta

                    if profit_pierdere >= 0:
                        pnl_text = f"🟢 +${profit_pierdere:.2f}"
                    else:
                        pnl_text = f"🔴 ${profit_pierdere:.2f}"

                    embed_portofoliu.add_field(name=f"{nume.capitalize()} ({cantitate} units)",
                                               value=f"💰 Bought at: ${pret_achizitie}\n📈 Current Price: ${pret_live}\n📊 P&L: {pnl_text}",
                                               inline=False)

                    await asyncio.sleep(1.5)
                profit_total = valoare_totala_curenta - valoare_totala_investita
                semn_total = "🟢 +" if profit_total >= 0 else "🔴 "
                embed_portofoliu.description = (
                    f"💵 Total Invested: **{valoare_totala_investita:.2f}$**\n"
                    f"💎 Current Value: **{valoare_totala_curenta:.2f}$**\n"
                    f"📉 Total Profit/Loss: **{semn_total}{profit_total:.2f}$**"
                )
                await message.channel.send(embed=embed_portofoliu)
TOKEN =  "PASTE_TOKEN_HERE"

client.run(TOKEN)