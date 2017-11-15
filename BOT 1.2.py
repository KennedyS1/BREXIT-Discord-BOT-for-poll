""""UPDATE V1.2
-Added a lot of functions to make the code more readable and modifiable
-Added an option to ask if the poll launcher wants the poll to end one hour after the quorum is reached
-Fixed some english mistakes
-Added a countdown option. It saves every countdown on a local file called countdown.json
"""

import discord
import asyncio
import datetime
import json
client = discord.Client()

#defining variables
self = None
choices_list = []
allowed_to_poll = []
poll_mode_enable = False
tmp_correct_answer_entered = False
end_poll_time_enable = False
poll_end_on_hour = False
poll_verification = False
poll_result_per_voter = {}
poll_result_per_choice = {}
voters_list = []
voters_has_voted = {}
voters_result_embed_text = ''
Quorum_warning_sent = False
hour_verification = True
valid_date_is_entered = True
date_verification = True
poll_end_on_date = False

posting_channel = client.get_channel('373099584211255297')
countdown_mode_enable = False
countdown = {}


#defining functions
async def poll_status(channel): #just posting the result in Wings' channel
    global poll_result_embed, status_channel
    title_text = 'Status for ' + str(title)
    poll_result_embed = discord.Embed(title=title_text, description='',color=0xFF0000)  # creating the embed result poll
    choice_result_embed_text = ''
    voters_result_embed_text = ''
    for choice in range(1, nb_choices + 1):
        voters_result_embed_text += str(poll_result_per_choice[choice]) + ' or ' + str(int(poll_result_per_choice[choice] * 10000 / len(poll_result_per_voter)) / 100) + "%\n"
    for i in range(len(choices_list)):
        choice_result_embed_text += '\n' + choices_list[i]
    poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
    poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)
    await client.send_message(channel, embed=poll_result_embed)
async def poll_close(): #posting result and disable the poll_mode
    global poll_mode_enable, poll_result_per_choice, poll_result_per_voter, choices_list
    title_text = 'Results for ' + str(title)
    poll_result_embed = discord.Embed(title=title_text, description='',color=0xFF0000)  # creating the embed result poll
    choice_result_embed_text = ''
    voters_result_embed_text = ''
    for choice in range(1, nb_choices + 1):
        voters_result_embed_text += str(poll_result_per_choice[choice]) + ' or ' + str(int(poll_result_per_choice[choice] * 10000 / len(poll_result_per_voter)) / 100) + "%\n"
    for i in range(len(choices_list)):
        choice_result_embed_text += '\n' + choices_list[i]
    poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
    poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)
    await client.send_message(client.get_channel('372306987641339904'), embed=poll_result_embed) #CHANGE THAT TO CHANGE WHERE THE POLL'S RESULT IS POSTED
    poll_mode_enable = False
    poll_result_per_voter = {}
    poll_result_per_choice = {}
    choices_list = []
    for member in voters_list:
        voters_has_voted[member] = False
async def poll_setup_title():
    global title
    await client.send_message(poll_launcher, "What is the title of the Poll ?")
    tmp_title = await client.wait_for_message(author=poll_launcher)
    title = tmp_title.content
async def poll_setup_nb_choices(): #Define how many choices there is + add a value of 0 voters for every choice
    global nb_choices
    await client.send_message(poll_launcher, "How many choices are there ?")
    nb_choices_is_integer = False
    while nb_choices_is_integer != True:  # Checking that it is actually an integer
        try:
            tmp_nb_choices = await client.wait_for_message(author=poll_launcher)
            nb_choices = int(tmp_nb_choices.content)
            nb_choices_is_integer = True
        except:
            await client.send_message(poll_launcher, "Please, enter an integer")
    for i in range(1, nb_choices + 1):  # creating a dictionary with a value of 0 for every choice
        poll_result_per_choice[i] = 0
async def poll_setup_every_choices():
    for i in range(nb_choices):
        await client.send_message(poll_launcher, "What is choice number " + str(i + 1) + " ?")
        tmp_choices_list = await client.wait_for_message(author=poll_launcher)
        choices_list.append(tmp_choices_list.content)
async def poll_setup_stop_on_time():
    global end_poll_time_enable
    await client.send_message(poll_launcher,"Should the poll end after a certain time ? yes/no (default is waiting for +poll_end)")
    tmp_end_poll_time_enable = await client.wait_for_message(author=poll_launcher)
    tmp_correct_answer_entered = False
    while tmp_correct_answer_entered != True:
        try:
            if tmp_end_poll_time_enable.content.lower() == "yes":
                end_poll_time_enable = True
                tmp_correct_answer_entered = True
            elif tmp_end_poll_time_enable.content.lower() == "no":
                end_poll_time_enable = False
                tmp_correct_answer_entered = True
            else:
                await client.send_message(poll_launcher,"Sorry, I didn't understand, please type \"yes\" or \"no\"")
                tmp_end_poll_time_enable = await client.wait_for_message(author=poll_launcher)
        except:
            await client.send_message(poll_launcher,"Sorry, I didn't understand, please type \"yes\" or \"no\"")
            tmp_end_poll_time_enable = await client.wait_for_message(author=poll_launcher)
async def poll_setup_poll_end_on_hour():
    global nb_hour_before_poll_end, poll_end_on_hour
    try:
        nb_hour_before_poll_end = int(tmp_time_when_poll_end.content)
        poll_end_on_hour = True
    except:
        await client.send_message(poll_launcher,'Sorry, I couldn\'t understand the date or the ammount of hours, please try again')
        await client.wait_for_message(author=poll_launcher)
async def poll_setup_poll_end_on_day():
    global poll_end_on_date, tmp_time_when_poll_end, sleep
    poll_end_on_date = True
    valid_date_is_entered = False
    while valid_date_is_entered == False:
        try:
            argument_day = int(tmp_time_when_poll_end.content[:2])
            argument_month = int(tmp_time_when_poll_end.content[3:])
            argument_year = 2017
            await client.send_message(poll_launcher, 'Please enter an hour in the following format \'hh:mm\'')
            tmp_hour_when_poll_end = await client.wait_for_message(author=poll_launcher)
            argument_hour = int(tmp_hour_when_poll_end.content[:2])
            argument_minute = int(tmp_hour_when_poll_end.content[3:])
            date_when_poll_end = datetime.datetime(argument_year, argument_month, argument_day, argument_hour,argument_minute, 0)
            current_date = datetime.datetime.now()
            sleep = (date_when_poll_end - current_date).total_seconds()
            if sleep > 0:
                valid_date_is_entered = True
            else:
                await client.send_message(poll_launcher, 'The poll can\'t end in the past')
                tmp_time_when_poll_end = await client.wait_for_message(author=poll_launcher)
        except:
            await client.send_message(poll_launcher, 'Sorry I could\'t understand the date')
            tmp_time_when_poll_end = await client.wait_for_message(author=poll_launcher)
async def poll_setup_embed():
    global poll_embed
    poll_embed_description = ''
    for i in range(nb_choices):
        poll_embed_description += "`" + str(i + 1) + "` " + choices_list[i] + "\n"
    poll_embed = discord.Embed(title=title, description=poll_embed_description, color=0xFF0000)
async def poll_setup_end_1hour_after_quorum_reached():
    global poll_end_1hour_after_quorum_reached
    await client.send_message(poll_launcher, 'Do you want the poll to end one hour after the Quorum (75%) is reached ? (yes/no)')
    tmp_end_poll_1_hour_after_quorum_reached = await client.wait_for_message(author=poll_launcher)
    tmp2_correct_answer_entered = False
    while tmp2_correct_answer_entered != True:
        try:
            if tmp_end_poll_1_hour_after_quorum_reached.content.lower() == "yes":
                poll_end_1hour_after_quorum_reached = True
                tmp2_correct_answer_entered = True
            elif tmp_end_poll_1_hour_after_quorum_reached.content.lower() == "no":
                poll_end_1hour_after_quorum_reached = False
                tmp2_correct_answer_entered = True
            else:
                await client.send_message(poll_launcher, "`Error 1`Sorry, I didn't understand, please type \"yes\" or \"no\"")
                tmp_end_poll_1_hour_after_quorum_reached = await client.wait_for_message(author=poll_launcher)
        except:
            await client.send_message(poll_launcher, "`Error 2`Sorry, I didn't understand, please type \"yes\" or \"no\"")
            tmp_end_poll_1_hour_after_quorum_reached = await client.wait_for_message(author=poll_launcher)






@client.event
async def on_ready():
    global voters_list
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #defining a way to access every role easily
    Administrator_role = discord.utils.get(client.get_server("274504339127664650").roles, name='Administrator')
    Inviters_role = discord.utils.get(client.get_server("274504339127664650").roles, name='Inviters')
    Voting_members_role = discord.utils.get(client.get_server("274504339127664650").roles, name='Voting Members')
    Wings_role = discord.utils.get(client.get_server("274504339127664650").roles, name='Wings')
    #make a list with every voters
    for member in client.get_server("274504339127664650").members:
        if Voting_members_role in member.roles:
            voters_list.append(member)
    #making a list of id of everyone allowed to start and end a poll
    for member in client.get_server("274504339127664650").members:
        if Administrator_role in member.roles or Inviters_role in member.roles or Wings_role in member.roles:
            allowed_to_poll.append(member.id)

@client.event
async def on_message(message):
    global poll_mode_enable, Quorum_warning_sent, poll_launcher, hour_verification,poll_end_on_hour,nb_hour_before_poll_end, nb_choices, title,valid_date_is_entered, poll_end_on_date, date_verification, sleep, poll_embed, tmp_time_when_poll_end,date_when_countdown_end
    if message.author.id != '364077741550731264':
        if message.content.startswith('+countdown') and any(i in [':', '/'] for i in message.content) == False :
            if message.server == None:
                await client.send_message(message.author, 'Sorry but poll cannot be accessed throught pms')
            else:
                if message.content.startswith == '+countdown_delete':
                    await client.send_message(message.channel, 'Enter the title of the countdown you want to delete')
                    title_to_delete = await client.wait_for_message(channel=message.channel)
                    del countdown[message.server][title_to_delete.content]
                    await client.send_message(message.channel, 'Countdown successfully deleted')
                else:
                    title = message.content[11:]
                    valid_countdown_date_is_entered = False
                    try:
                        if countdown[message.server][title]['enable'] == False:
                            int('string') #making an error so it switches in except
                        elif countdown[message.server][title]['enable'] == True:
                            current_date = datetime.datetime.now()
                            tmp_time_remaining = countdown[message.server][title]['date'] - current_date
                            if tmp_time_remaining <= datetime.timedelta():
                                countdown[message.server][title]['enable'] = False
                                await client.send_message(message.channel, 'This poll has already ended')
                            else:
                                tmp_time_remaining = str(tmp_time_remaining)
                                await client.send_message(message.channel, 'Time remaining: ' + tmp_time_remaining[:16])
                    except:
                        while valid_countdown_date_is_entered == False:
                            try:
                                await client.send_message(message.channel, 'Please enter the date where the countdown will end in the following format: +countdown dd/mm/yyyy hh:mm')
                                countdown[message.server] = {}
                                countdown[message.server][title] = {}
                                message_with_date = await client.wait_for_message(channel=message.channel, author=message.author)
                                countdown[message.server][title]['day'] = int(message_with_date.content[11:13])
                                countdown[message.server][title]['month'] = int(message_with_date.content[14:16])
                                countdown[message.server][title]['year'] = int(message_with_date.content[17:21])
                                countdown[message.server][title]['hour'] = int(message_with_date.content[22:24])
                                countdown[message.server][title]['minute'] = int(message_with_date.content[25:27])
                                countdown[message.server][title]['date'] = datetime.datetime(countdown[message.server][title]['year'], countdown[message.server][title]['month'], countdown[message.server][title]['day'], countdown[message.server][title]['hour'], countdown[message.server][title]['minute'], 0)
                                current_date = datetime.datetime.now()
                                tmp_time_remaining = (countdown[message.server][title]['date'] - current_date)
                                try:
                                    if tmp_time_remaining.total_seconds() <= 0:
                                        await client.send_message(message.channel, 'The poll is ending in the past, please try again')
                                    else:
                                        nothing = int('string')
                                except:
                                    await client.send_message(message.channel, 'Time remaining: ' + str(tmp_time_remaining)[:str(tmp_time_remaining).index('.')])
                                    valid_countdown_date_is_entered = True
                                    countdown[message.server][title]['enable'] = True
                            except:
                                message = await client.wait_for_message(author=message.author, channel=message.channel)
        if poll_mode_enable == False:
            if message.content.startswith('+poll'): #what happen if a poll is called
                if message.author.id in allowed_to_poll or message.author.id == "172423919041511424":#checking if the user is allowed to launch a poll
                    if message.content.startswith('+poll_verbose'): #checking if the poll is in verbose mode
                        poll_launcher = message.author
                        await poll_setup_title()#defining poll title
                        await poll_setup_nb_choices()# defining number of choices + handling errors + creating a dictionnary with a value of 0 for every choice
                        await poll_setup_every_choices()# defining every choices
                        await poll_setup_stop_on_time()#defining if the poll should end at after a certain ammount of time
                        if end_poll_time_enable:
                            global tmp_time_when_poll_end
                            await client.send_message(poll_launcher,'Please enter a number of hours or a date in the following format \'dd/mm\'')
                            tmp_time_when_poll_end = await client.wait_for_message(author=poll_launcher)
                            if '/' in tmp_time_when_poll_end.content:
                                await poll_setup_poll_end_on_day()
                            else:
                                await poll_setup_poll_end_on_hour()
                        await poll_setup_end_1hour_after_quorum_reached()
                        await poll_setup_embed()# creating an embed
                        # checking if there isn't any typo
                        await client.send_message(poll_launcher, embed=poll_embed)
                        await client.send_message(poll_launcher, "This is the actual poll, what do you want to do ? (p : post, m : modify, c : cancel)")
                        tmp_poll_verification_text = await client.wait_for_message(author=poll_launcher)
                        poll_verification = False
                        while poll_verification != True:
                            poll_verification_text = tmp_poll_verification_text.content
                            try:
                                if poll_verification_text == 'p' or poll_verification_text == 'post':
                                    await client.send_message(poll_launcher, "Posting the poll !")
                                    await client.send_message(client.get_channel('372306987641339904'), embed=poll_embed)
                                    await client.send_message(client.get_channel('372306987641339904'), '<@&372313160801320971>')
                                    poll_mode_enable = True
                                    for members in voters_list:  # Setting the fact that no one voted yet
                                        voters_has_voted[members] = False
                                    poll_verification = True
                                    if poll_end_on_date == True:
                                        await asyncio.sleep(sleep)
                                        await poll_close()
                                    elif poll_end_on_hour == True:
                                        await asyncio.sleep(nb_hour_before_poll_end * 3600)
                                        await poll_close()


                                elif poll_verification_text == 'm' or poll_verification_text == 'modify':
                                    await client.send_message(poll_launcher,'Sorry we haven\'t developped this feature yet but you can cancel the poll and create a new one.')
                                    # need to be done but like what do you want to change ? and then re-prompt functions
                                elif poll_verification_text == 'c' or poll_verification_text == 'cancel':
                                    await client.send_message(poll_launcher, 'Poll deleted, have a nice day !')
                                    poll_verification = True
                                else:
                                    await client.send_message(poll_launcher,'`Error 1` Sorry I don\'t undestand, please enter one of the following:\n' +
                                                                             'p\nm\nc')
                                    tmp_poll_verification_text = await client.wait_for_message(author=poll_launcher)
                            except:
                                await client.send_message(poll_launcher,'Sorry I don\'t undestand, please enter one of the following:\n' +
                                                                         'p\nm\nc')
                                tmp_poll_verification_text = await client.wait_for_message(author=poll_launcher)







                    else: #if the poll isn't normal, send an error message in pm
                        await client.send_message(message.author, "Unknown command, the command available commands are\n" +
                                                                  "+poll\n" +
                                                                  "+poll_verbose")
                else: #if the member isn't allowed to launch a poll
                    await client.send_message(message.author, "Sorry you aren't allowed to launch poll on brexit's server")
        elif poll_mode_enable == True:
            if message.channel == client.get_channel('372306987641339904') or message.server == None or message.channel == client.get_channel('372781706370875392'): #making sure the message in a PM or in the client.get_channel('373099584211255297')
                if message.content.lower() == '+poll_end':
                    if message.author.id in allowed_to_poll or message.author.id == '172423919041511424':
                        await poll_close()
                    else:
                        await client.send_message(message.author, 'Sorry, you aren\'t allowed to end a poll')
                elif message.content == '+poll' or message.content == '+poll_verbose': #Checking if someone wants to call another poll
                    await client.send_message(message.author, 'You can\'t call a poll: Another poll is already running')
                elif message.content.lower() == '+poll_stats':
                    if message.author.id in allowed_to_poll or message.author.id == '172423919041511424':
                        await poll_status(channel=message.channel)
                    else:
                        await client.send_message(message.author,'Sorry, you aren\'t allowed to request a status of the running poll.')
                elif message.content.lower() == '+poll_member_check':
                    if message.author.id in allowed_to_poll or message.author.id == '172423919041511424':
                        voter_list = ''
                        for voter in voters_has_voted:
                            if voters_has_voted[voter] == False:
                                voter_list += '<@'+ str(voter.id) + '>\n'
                        await client.send_message(client.get_channel('372781706370875392'), voter_list)
                    else:
                        await client.send_message(message.author,'Sorry, you aren\'t allowed to request a member check of the running poll.')
                else:
                    try:#Checking if the message is an actual vote (is it an integer ?)
                        if int(message.content) in range(1,nb_choices+1):#Checking if the message is an actual vote (is it in the range of the choice ?)
                            if message.author in voters_list: #Checking that the voter is allowed to vote
                                if message.author not in poll_result_per_voter:#Checking if the user haven't voted yet
                                    poll_result_per_voter[message.author] = message.content #add a vote to the person
                                    poll_result_per_choice[int(message.content)] += 1
                                    if message.server == None: #checking if it's DM
                                        await client.send_message(message.author, 'You voted successfully')
                                        await client.send_message(client.get_channel('372781706370875392'),str(message.author.name) + ' voted.\n' + str(len(poll_result_per_voter)) + ' votes yet which is equal to ' + str(int(len(poll_result_per_voter) * 10000 / len(voters_list)) / 100) + '% of the voters')
                                    else:
                                        voting_confirmation = await client.send_message(message.channel, str(message.author.name) + ' voted successfully')
                                        await client.delete_message(message)  # delete the message
                                        await client.send_message(client.get_channel('372781706370875392'),str(message.author.name) + ' voted.\n' + str(len(poll_result_per_voter)) + ' votes yet which is equal to ' + str(int(len(poll_result_per_voter) * 10000 / len(voters_list)) / 100) + '% of the voters')
                                        await asyncio.sleep(5)
                                        await client.delete_message(voting_confirmation)

                                    voters_has_voted[message.author] = True



                                    if len(voters_list) == len(poll_result_per_voter): #if everyone voted
                                        await client.send_message(poll_launcher, 'Everyone voted in for the following poll: ' + str(title) + '. The poll will now close automatically')
                                        await poll_close()
                                    elif len(poll_result_per_voter)/len(voters_list) >= 0.75 and Quorum_warning_sent == False:
                                        if poll_end_1hour_after_quorum_reached:
                                            for voters in voters_list:
                                                if voters_has_voted[voters] == False:
                                                    await client.send_message(voters, 'Hey, the poll ' + str(title) + ' has reached a quorum, the poll will close in one hour')
                                            Quorum_warning_sent = True
                                            await asyncio.sleep(3600)
                                            await poll_close()
                                else: #if the voter already voted
                                    await client.send_message(message.author,'Sorry, you can\'t vote, you already voted')
                                    if message.server != None:
                                        await client.delete_message(message=message)  # delete the message
                            else: #if the voters isn't allowed to vote
                                await client.send_message(message.author, 'Sorry, but you aren\'t allowed to vote, please contact Wings to get the right to vote')
                                if message.server != None:
                                    await client.delete_message(message=message)  # delete the message
                        else: #if the message isn't a vote
                            if message.author.id != '150945326495301632':  # if the author isn't Wings
                                await client.send_message(message.author,'`Error 1` Sorry, but I couldn\'t understand your vote ')  # send a pm to guy that sen't a wrong message
                                if message.server != None:
                                    await client.delete_message(message=message)  # delete the message
                    except: #if the message isn't a vote
                        if message.author.id != '150945326495301632': #if the author isn't Wings
                            await client.send_message(message.author, '`Error 2` Sorry, but I couldn\'t understand your vote') #send a pm to guy that sen't a wrong message
                            if message.server != None:
                                await client.delete_message(message=message) #delete the message





client.run('INSERT_TOKEN_HERE')
