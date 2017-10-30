"""Update 1.1
-Allowing Wings to post messages without getting deleted
-Votes throught pms are accepted
-You can now use +poll_status
-Logging into Wings' text channel
-Feedback have been changed
-Poll ending once it reaches 100% participation
-Time based poll
-Number of voter is along a percentage (see +poll_end or +poll_status)"""

import discord
import asyncio
import datetime
client = discord.Client()

#defining variables
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
    global poll_mode_enable, Quorum_warning_sent, poll_launcher, hour_verification,poll_end_on_hour,nb_hour_before_poll_end, nb_choices, title,valid_date_is_entered, poll_end_on_date, date_verification, sleep
    def normal_poll():
        print('it needs to be done fak off')


    if poll_mode_enable == False:
        if message.content.startswith('+poll'): #what happen if a poll is called
            if message.author.id in allowed_to_poll or message.author.id == "172423919041511424":#checking if the user is allowed to launch a poll
                if message.content ==('+poll'): #Checking if a normal poll is requested
                    normal_poll()
                elif message.content.startswith('+poll_verbose'): #checking if the poll is in verbose mode
                    poll_launcher = message.author
                    await client.send_message(poll_launcher, "What is the title of the Poll ?")
                    tmp_title = await client.wait_for_message(author=poll_launcher)
                    title = tmp_title.content
                    # defining number of choices + handling errors + creating a dictionnary with a value of 0 for every choice
                    await client.send_message(poll_launcher, "How many choices are there ?")
                    nb_choices_is_integer = False
                    while nb_choices_is_integer != True:  # Checking that it is actually an integer
                        try:
                            tmp_nb_choices = await client.wait_for_message(author=poll_launcher)
                            nb_choices = int(tmp_nb_choices.content)
                            nb_choices_is_integer = True
                        except:
                            await client.send_message(poll_launcher, "Please, enter an integer")
                    for i in range(1,nb_choices+1):  # creating a dictionary with a value of 0 for every choice
                        poll_result_per_choice[i] = 0
                    # defining every choices
                    for i in range(nb_choices):
                        await client.send_message(poll_launcher, "What is the choice number " + str(i + 1) + " ?")
                        tmp_choices_list = await client.wait_for_message(author=poll_launcher)
                        choices_list.append(tmp_choices_list.content)

                    # defining if the poll should be stopped at a certain time
                    await client.send_message(poll_launcher,"When you should the poll end after a certain time ? yes/no (default is waiting for +poll_end)")
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
                                await client.send_message(poll_launcher, "Sorry, I didn't understand, please type \"yes\" or \"no\"")
                                tmp_end_poll_time_enable = await client.wait_for_message(author=poll_launcher)
                        except:
                            await client.send_message(poll_launcher,"Sorry, I didn't understand, please type \"yes\" or \"no\"")
                            tmp_end_poll_time_enable = await client.wait_for_message(author=poll_launcher)
                    # defining when the poll should stop
                    if end_poll_time_enable:
                        await client.send_message(poll_launcher,'Please enter a number of hours or a date in the following format \'dd/mm\'')
                        tmp_time_when_poll_end = await client.wait_for_message(author=poll_launcher)
                        if '/' in tmp_time_when_poll_end.content:
                            poll_end_on_date = True
                            valid_date_is_entered = False
                            while valid_date_is_entered == False:
                                #try:
                                argument_day = int(tmp_time_when_poll_end.content[:2])
                                argument_month = int(tmp_time_when_poll_end.content[3:])
                                argument_year = 2017
                                await client.send_message(poll_launcher, 'Please enter a date in the following format \'hh:mm\'')
                                tmp_hour_when_poll_end = await client.wait_for_message(author=poll_launcher)
                                argument_hour = int(tmp_hour_when_poll_end.content[:2])
                                argument_minute = int(tmp_hour_when_poll_end.content[3:])
                                date_when_poll_end = datetime.datetime(argument_year, argument_month, argument_day, argument_hour,argument_minute, 0)
                                current_date = datetime.datetime.now()
                                print('current date : ')
                                print(current_date)
                                print('date when poll end: ')
                                print(date_when_poll_end)
                                sleep = (date_when_poll_end - current_date).total_seconds()
                                print(sleep)
                                if sleep > 0:
                                    valid_date_is_entered = True
                                else:
                                    await client.send_message(poll_launcher, 'The poll can\'t end in the past')
                                    tmp_time_when_poll_end = await client.wait_for_message(author=poll_launcher)
                                #except:
                                #    await client.send_message(poll_launcher, 'Sorry I could\'t understand the date')
                                #    tmp_time_when_poll_end = await client.wait_for_message(author=poll_launcher)
                        else:
                            try:
                                nb_hour_before_poll_end = int(tmp_time_when_poll_end.content)
                                poll_end_on_hour = True

                            except:
                                await client.send_message(poll_launcher, 'Sorry, I couldn\'t understand the date or the ammount of hours, please try again')
                                await client.wait_for_message(author=poll_launcher)
                    # creating an embed
                    poll_embed_description = ''
                    for i in range(nb_choices):
                        poll_embed_description += "`" + str(i + 1) + "` " + choices_list[i] + "\n"
                    poll_embed = discord.Embed(title=title, description=poll_embed_description, color=0xFF0000)

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


                                poll_mode_enable = True
                                for members in voters_list:  # Setting the fact that everyone hasn't voted yet
                                    voters_has_voted[members] = False
                                poll_verification = True
                                if poll_end_on_date == True:
                                    await asyncio.sleep(sleep)
                                    # closing poll
                                    title_text = 'Results for ' + str(title)
                                    poll_result_embed = discord.Embed(title=title_text, description='',color=0xFF0000)  # creating the embed result poll
                                    choice_result_embed_text = ''
                                    voters_result_embed_text = ''
                                    for choice in range(1, nb_choices + 1):
                                        voters_result_embed_text += str(poll_result_per_choice[choice]) + "\n"
                                    for i in range(len(choices_list)):
                                        choice_result_embed_text += '\n' + choices_list[i]
                                    poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
                                    poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)

                                    await client.send_message(client.get_channel('373099584211255297'),embed=poll_result_embed)

                                    poll_mode_enable = False
                                elif poll_end_on_hour == True:
                                    await asyncio.sleep(nb_hour_before_poll_end * 3600)
                                    # closing poll
                                    title_text = 'Results for ' + str(title)
                                    poll_result_embed = discord.Embed(title=title_text, description='',color=0xFF0000)  # creating the embed result poll
                                    choice_result_embed_text = ''
                                    voters_result_embed_text = ''
                                    for choice in range(1, nb_choices + 1):
                                        voters_result_embed_text += str(poll_result_per_choice[choice]) + "\n"
                                    for i in range(len(choices_list)):
                                        choice_result_embed_text += '\n' + choices_list[i]
                                    poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
                                    poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)

                                    await client.send_message(client.get_channel('373099584211255297'),embed=poll_result_embed)

                                    poll_mode_enable = False


                            elif poll_verification_text == 'm' or poll_verification_text == 'modify':
                                print('Someone wanted to modify, add this feature pls')
                                await client.send_message(poll_launcher,'Sorry we haven\'t developped this feature yet but you can cancel the poll and create a new one.')
                                # need to be done but like what do you want to change ? and then re-prompt functions
                            elif poll_verification_text == 'c' or poll_verification_text == 'cancel':
                                await client.send_message(poll_launcher, 'Poll deleted, have a nice day !')
                            else:
                                await client.send_message(poll_launcher,'Sorry I don\'t undestand, please enter one of the following:\n' +
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
        if message.channel == client.get_channel('373099584211255297') or message.channel == client.get_channel('372306987641339904') or message.server == None or message.channel == client.get_channel('372781706370875392'): #making sure it's the channel that are specified
            if message.author.id != "364077741550731264" and message.author.id != '155149108183695360' and message.author.id != '116275390695079945':  # checking it's not a bot
                if message.content.lower() == '+poll_end':
                    if message.author.id in allowed_to_poll or message.author.id == '172423919041511424':
                        title_text = 'Results for ' + str(title)
                        poll_result_embed = discord.Embed(title=title_text, description='',color=0xFF0000)  # creating the embed result poll
                        choice_result_embed_text = ''
                        voters_result_embed_text = ''
                        for choice in range(1,nb_choices+1):
                            voters_result_embed_text += str(poll_result_per_choice[choice]) + ' or ' + str(int(poll_result_per_choice[choice]*10000/len(poll_result_per_voter))/100) + "%\n"
                        for i in range(len(choices_list)):
                            choice_result_embed_text += '\n' + choices_list[i]
                        poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
                        poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)


                        await client.send_message(client.get_channel('372306987641339904'), embed=poll_result_embed)


                        poll_mode_enable = False
                    else:
                        await client.send_message(message.author, 'Sorry, you aren\'t allowed to end a poll')


                elif message.content.lower() == '+poll_status':
                    if message.author.id in allowed_to_poll or message.author.id == '172423919041511424':
                        title_text = 'Actual status for ' + str(title)
                        poll_result_embed = discord.Embed(title=title_text, description='',color=0xFF0000)  # creating the embed result poll
                        choice_result_embed_text = ''
                        voters_result_embed_text = ''
                        for choice in range(1,nb_choices+1):
                            voters_result_embed_text += str(poll_result_per_choice[choice]) + ' or ' + str(int(poll_result_per_choice[choice] * 10000 / len(poll_result_per_voter)) / 100) + "\n"
                        for i in range(len(choices_list)):
                            choice_result_embed_text += '\n' + choices_list[i]
                        poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
                        poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)
                        await client.send_message(message.channel, embed=poll_result_embed)
                    else:
                        await client.send_message(message.author, 'Sorry, you aren\'t allowed to request a status of the running poll.')


                elif message.content == '+poll' or message.content == '+poll_verbose': #Checking if someone wants to call another poll
                    await client.send_message(message.author, 'You can\'t call a poll: Another poll is already running')
                elif message.content.startswith('+poll'):
                    await client.send_message(message.author, 'Error: Unknown command')
                else:
                    try:#Checking if the message is an actual vote (is it an integer ?)
                        if int(message.content) in range(1,nb_choices+1):#Checking if the message is an actual vote (is it in the range of the choice ?)
                            if message.author in voters_list: #Checking that the voter is allowed to vote
                                if message.author not in poll_result_per_voter:#Checking if the user haven't voted yet
                                    poll_result_per_voter[message.author] = message.content #add a vote to the person
                                    poll_result_per_choice[int(message.content)] += 1
                                    if message.server == None: #checking if it's DM
                                        await client.send_message(message.author, 'You voted successfully')
                                    else:
                                        voting_confirmation = await client.send_message(message.channel, str(message.author.name) + ' voted successfully')
                                        await client.delete_message(message)  # delete the message
                                        await asyncio.sleep(5)
                                        await client.delete_message(voting_confirmation)
                                    await client.send_message(client.get_channel('372781706370875392'), str(message.author.name) + ' voted.\n' +
                                                                                                        str(len(poll_result_per_voter)) + ' votes yet which is equal to ' + str(int(len(poll_result_per_voter)*10000/len(voters_list))/100) + '% of the voters')


                                    voters_has_voted[message.author] = True
                                    if len(voters_list) == len(poll_result_per_voter): #if everyone voted
                                        await client.send_message(poll_launcher, 'Everyone voted in for the following poll: ' + str(title) + '. The poll will now close automatically')
                                        title_text = 'Results for ' + str(title)
                                        poll_result_embed = discord.Embed(title=title_text, description='',color=0xFF0000)  # creating the embed result poll
                                        choice_result_embed_text = ''
                                        voters_result_embed_text = ''
                                        for choice in range(1, nb_choices + 1):
                                            voters_result_embed_text += str(poll_result_per_choice[choice]) + "\n"
                                        for i in range(len(choices_list)):
                                            choice_result_embed_text += '\n' + choices_list[i]
                                        poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
                                        poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)


                                        await client.send_message(client.get_channel('372306987641339904'),embed=poll_result_embed)


                                        poll_mode_enable = False
                                    elif len(poll_result_per_voter)/len(voters_list) >= 0.75 and Quorum_warning_sent == False:
                                        for voters in voters_list:
                                            if voters_has_voted[voters] == False:
                                                await client.send_message(voters, 'Hey, the poll ' + str(title) + ' has reached a quorum, the poll will close in one hour')
                                        Quorum_warning_sent = True
                                        await asyncio.sleep(3600)
                                        #closing the poll
                                        title_text = 'Results for ' + str(title)
                                        poll_result_embed = discord.Embed(title=title_text, description='',
                                                                          color=0xFF0000)  # creating the embed result poll
                                        choice_result_embed_text = ''
                                        voters_result_embed_text = ''
                                        for choice in range(1, nb_choices + 1):
                                            voters_result_embed_text += str(poll_result_per_choice[choice]) + "\n"
                                        for i in range(len(choices_list)):
                                            choice_result_embed_text += '\n' + choices_list[i]
                                        poll_result_embed.add_field(name='Choices', value=choice_result_embed_text)
                                        poll_result_embed.add_field(name='Voters', value=voters_result_embed_text)


                                        await client.send_message(client.get_channel('372306987641339904'),embed=poll_result_embed)


                                        poll_mode_enable = False
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





client.run('MzY0MDc3NzQxNTUwNzMxMjY0.DLKhhw.7Mj1jqZjtMXqkQo61oXPy_T872I')