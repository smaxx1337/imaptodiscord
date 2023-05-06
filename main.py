import json
from imap_tools import MailBox, AND
from discord_webhook import DiscordWebhook, DiscordEmbed

f = open('config.json')
data = json.load(f)

imap_host = data["hostname"]
imap_user = data["username"]
imap_pass = data["password"]
webhook = DiscordWebhook(url=data["webhook"])

with MailBox(imap_host).login(imap_user, imap_pass, 'INBOX') as mailbox:
    for msg in mailbox.fetch(AND(seen=False), mark_seen=True):

        date_string = str(msg.date)
        sender = msg.from_
        cc = msg.cc
        subject = msg.subject
        text = msg.text

        embed = DiscordEmbed(title=subject, description=text)
        embed.set_author(name=sender)
        embed.set_footer(text=date_string)
    
        webhook.add_embed(embed)
        response = webhook.execute()