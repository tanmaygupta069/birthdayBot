import discord
from replit import db
from discord.ext import commands
from token_2 import token
# from datetime import datetime, timezone,date
import datetime
import pytz
import asyncio
from alive import alive

client = commands.Bot(command_prefix="bbot ", intents=discord.Intents.all())
client.remove_command("help")
channel = client.get_channel(884889940817760256)
channel1 = 0
guild1 = 0
l = []


@client.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        description=
        "This is the list of commands you can use for this bot. *Default command prefix* `bbot<command>`",
        color=discord.Color.blue())
    embed.set_author(name="Here for you help ✨", icon_url=client.user.avatar)
    embed.add_field(
        name="`set`",
        value=
        "Takes your birthdate like `set <dd/mm/yyyy>` and wishes you when it arrives.",
        inline=False)
    embed.add_field(
        name="`delete`",
        value=
        "Deletes your birthdate from the database `delete <username to be deleted without tag>`",
        inline=False)
    embed.add_field(
        name="`list`",
        value=
        "Displays the list of people entered their birthdate in this server `list` ",
        inline=False)
    embed.add_field(name="‍", value="‍‍‍‍‍‍‍‍‍‍‍‍‍‍", inline=False)
    embed.add_field(name="Moderator Commands",
                    value="Requires a special role to use this commands.",
                    inline=False)
    embed.add_field(name="`delete_db`",
                    value="Delete the whole database.",
                    inline=False)
    embed.add_field(name="`reset`",
                    value="Resets database to default vales.",
                    inline=False)
    embed.add_field(name="`info`",
                    value="Terminal command can't be seen by normal users.",
                    inline=False)
    await ctx.message.author.send(embed=embed)
    await ctx.send("Check your dm.")


@client.command(name="set")
async def set(ctx, day: int, month: int, year: int):
    now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    print("now : ", now)
    print(now.replace(tzinfo=None))
    today1 = now.strftime("%d %m %y")
    bdate = datetime.date(year=now.year, month=month, day=day)
    bday = bdate.strftime("%d %m %y")

    print(bdate)
    if bday < today1:
        print("smaller")
        bdate = bdate.replace(year=now.year + 1)
    elif bday == today1:
        print("in")
        await asyncio.sleep(2)
        embed1 = discord.Embed(
            description=
            f"Wishing {ctx.message.author.mention} a happy and lovely day ahead.",
            color=discord.Colour.blue())
        embed1.set_thumbnail(url=ctx.message.author.avatar)
        embed1.set_author(name="Happy Birthday ✨")
        channel = client.get_channel(884889940817760256)
        await channel.send(embed=embed1)

    bdateStr = bdate.strftime("%A %d. %B %Y")
    await ctx.send(f"Noted,your Birthday is on `{bdateStr}`.")

    bdateStr1 = bdate.strftime("%d %m %y")

    db[str(ctx.message.author).split("#")[0]] = [bdateStr1, 0]


@client.command(name="reset")
async def reset(ctx):
    guild = guild1
    admin = discord.utils.get(guild.roles, name="admin")
    if admin in ctx.message.author.roles:
        for dates in db.values():

            try:
                if dates == "":
                    raise Exception("`The database is empty.`")
            except:
                print('Expection')
                await ctx.send(Exception)
            dates[1] = 0
            print("reset done")

        await ctx.send("`Reseted dates.`")
    else:
        await ctx.send("`You don't have the permission to use this command.`")
        return


@client.command(name="info")
async def info(ctx):
    for names in db.keys():
        print(names, " ", db[names][0], " ", db[names][1])
    await ctx.send("`Terminal command.`")


@client.command(name="list")
async def list(ctx):
    count = 1
    embed2 = discord.Embed(title="", color=discord.Colour.blue())
    for names in db.keys():
        # if names in guild:

        print(count)
        embed2.add_field(name=str(count) + ". " + str(names).split('#')[0] +
                              "           " + str(db[names])[21:23] + "-" +
                              str(db[names])[24:26] + "-" + str(db[names])[27:29],
                         value='‍‍',
                         inline=False)
        count += 1
    try:
        await ctx.send(embed=embed2)
    except:
        await ctx.send("`The database is probably empty`")


@client.command(name="delete")
async def delete(ctx, name: str, surname: str = ""):
    count = 0
    channel = channel1
    guild = guild1
    admin = discord.utils.get(guild.roles, name="admin")
    if admin in ctx.message.author.roles:
        for key in db.keys():
            if str(key).split("#")[0] == name + " " + surname or str(key).split(
                    "#")[0] == name:
                print(name + " " + surname)
                del db[key]
                print("Entry deleted.")
                await channel.send("`Entry deleted.`")
    else:
        for key in db.keys():
            if str(ctx.message.author).split("#")[0] == name or str(
                    ctx.message.author).split("#")[0] == name + " " + surname:
                if str(key).split("#")[0] == name + " " + surname or str(key).split(
                        "#")[0] == name:
                    del db[key]
                    await ctx.send("`Your Entry deleted.`")
            else:
                count += 1
                if count == 1:
                    await ctx.send("`Permission denied.Need to be a moderator.`")


@client.command(name="delete_db")
async def delete_db(ctx):
    channel = channel1
    guild = guild1
    admin = discord.utils.get(guild.roles, name="admin")
    if admin in ctx.message.author.roles:
        for key in db.keys():
            del db[key]
        await channel.send("`Database deleted.`")
    else:
        await channel.send("`Permission denied.Reason(moderator commands)`")


@client.event
async def on_ready():
    print(f"You have logged in as {client.user}.")
    await main()


@client.command(name="config")
async def config(ctx, guild_id, channel_id):
    guild1 = client.get_guild(guild_id)
    channel1 = client.get_channel(channel_id)
    await ctx.send("Channel and guild set.")


async def main():
    while True:
        print("checking!")
        now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        today = now.strftime("%d %m")
        for dates in db.values():
            print(dates[0], " ", today)
            if dates[0][0:5] == str(today):
                print("date found")
                guild = client.get_guild(690119909119754245)
                for member in guild.members:
                    for name in db.keys():
                        if db[name][0] == dates[0]:
                            print("something")
                            if str(member).split("#")[0] == str(name):
                                print("member found")
                                if db[name][1] == 0 and name not in l:
                                    print("uu")
                                    db[name][1] = 1
                                    embed = discord.Embed(
                                        description=f"Wishing {member.mention} a happy Birthday.",
                                        color=discord.Colour.blue())
                                    embed.set_thumbnail(url=member.avatar)
                                    embed.set_author(name="Happy Birthday ✨")
                                    channel = client.get_channel(884889940817760256)
                                    await channel.send(embed=embed)
                                    print("wished.")
                                    l.append(name)
                                    print(l)

        else:
            tomrow = datetime.datetime(
                year=now.year,
                month=now.month,
                day=now.day + 1,
                hour=0,
                minute=0,
                second=0,
            )
            print("tommorow : ", tomrow)
            print("now:", now)
            wait_time = (tomrow - now.replace(tzinfo=None)).total_seconds()
            print("No birthdays")
            print(f"sleeping for {round(int(wait_time) / 3600, 2)} hours")

            await asyncio.sleep(wait_time)
            for n in l:
                print("in")
                db[n][1] = 0
            l.clear()
            print("erased wished from db")


alive()
client.run(token)

if __name__ == "__main__":
    main()
