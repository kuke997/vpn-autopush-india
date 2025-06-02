from telegram import Bot, ParseMode

def push_to_channel(bot_token, channel_id, clash_url, v2ray_url, ss_url):
    bot = Bot(token=bot_token)
    text = f"""
🚀 **Free VPN for India – Auto Updated Daily** 🇮🇳

✅ Works with:
- 🌀 [Clash Config]({clash_url})
- ⚡ [V2Ray Sub]({v2ray_url})
- 🔐 [Shadowsocks Sub]({ss_url})

> Unblock Twitter (X), Porn, Reddit, Telegram, 1xBet & more.

#vpn #freevpn #clash #v2ray #shadowsocks #vpnindia
"""
    bot.send_message(chat_id=channel_id, text=text.strip(), parse_mode=ParseMode.MARKDOWN)
