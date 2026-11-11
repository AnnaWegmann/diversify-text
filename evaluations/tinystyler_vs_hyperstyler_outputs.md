# TinyStyler vs HyperStyler outputs

Both models rewrote the same 8 input texts in each of TinyStyler's 21 styles, one sample per text and style, each with its own default settings.

## informal

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | i think we should leave early tomorrow to avoid traffic. | oh i think we should leave early tomorrow to avoid traffic? |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | city council just decided to delay the bike lane project until spring....yeah. | the city council decided to delay the bike lane project until next spring? |
| Thanks for the update, I'll take a look at the report this afternoon. | i'll take a look at the report this afternoon thanks! | i will check the report today after the update. |
| Could you tell me where the nearest pharmacy is? | could you tell me where the nearest pharmacy is tho? | where is the nearest pharmacy to you? |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | my sister adopted a small grey cat last week and it rules the whole apartment lol. | idk my sister adopted a small grey cat last week and it already rules the apartment |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | experiment failed twice before we noticed the sensor was upside down. | i know the sensor is installed upside down and the experiment failed twice before i noticed it |
| Honestly the movie was fine, but the ending made no sense to me. | the movie was fine but the ending didnt make sense to me xD | the movie was fine but the ending didnt make sense to me, but i fucking hate this movie. |
| Please remember to submit your expense claims before the end of the month. | yea submit your expense claims before end of month please. | if you need an expense claim you should submit it before the end of the month |

## formal

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow to avoid traffic. | I agree. But we should leave early tomorrow, and avoid the traffic's shitstorm. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | I'm guessing the city council decided to delay the bike lane project until next spring. | The city council voted to delay the bike lane project until next spring. |
| Thanks for the update, I'll take a look at the report this afternoon. | I'll take a look at the report this afternoon. | I'll look at the report this afternoon. I'm also currently using my reinstalled reinstaller. I have an updated version, hoping he fixes it. I have the same issue with reinstalling my computer! |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is in this area. | You could tell me where the nearest pharmacy is? |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week, and it rules the apartment. | I also adopted a small grey cat last week and it already rules the apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | We noticed the sensor was installed upside down before the experiment failed twice. | I noticed the sensor had been installed upside down, the experiment failed twice. |
| Honestly the movie was fine, but the ending made no sense to me. | I enjoyed the movie, but the ending made no sense to me. | For me the ending made no sense, which was the movie. |
| Please remember to submit your expense claims before the end of the month. | Please submit your expense claims before the end of the month. | If you want to submit expense claims before the end of the month. |

## question

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | Why not leave early tomorrow? I think it would save us from traffic. | Where do you go? I want to avoid traffic, and leave early. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | You know the city council voted to delay the new bike lane project until next spring? That was Tuesday. | How long is the bike lane project? The city council voted to delay it until next spring. |
| Thanks for the update, I'll take a look at the report this afternoon. | What is the report? I will take a look at it this afternoon. | Where are you located? I'll check out the report this afternoon, thanks for the update. |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is? I have a smear of a smear on my forehead. | Where is the nearest pharmacy? I have a question. |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week. It rules the whole apartment. | Where do you live? For my sister she got a small grey cat last week, and it rules the whole apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | What about the sensor installed upside down? We failed the experiment twice before we noticed. | Where are you? The experiment failed twice before we noticed the sensor is installed upside down. |
| Honestly the movie was fine, but the ending made no sense to me. | Is the ending a joke? The movie was fine, but the ending made no sense. | Where are you getting your rewatched? I liked the movie, but the ending was very bad for me. |
| Please remember to submit your expense claims before the end of the month. | You have to submit your expense claims before the end of the month? I think that is the deadline. | What time does your claim go out? You need to submit it at the end of the month. |

## question_answer_forum

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow to avoid traffic. Are you planning on staying in the same hotel for the whole weekend? | I was going to say this but: I think we should leave early tomorrow to avoid traffic. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | Is it true that the city council voted to delay the new bike lane project until next spring? | What is the reasoning behind the city council delaying the new bike lane project until next spring? A new bike lane was planned for the city. |
| Thanks for the update, I'll take a look at the report this afternoon. | What is the report on this? I will take a look at it this afternoon. | I just need to get to this: I'll take a look at the report this afternoon after the update, but thanks for the update. |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the closest pharmacy is? I would love to go to a pharmacy that has a good selection, but not a good price. | Thanks for this: could you tell me where the nearest pharmacy is? |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week and it rules the apartment. If you can't keep it out of the house, should you move it? | What is the difference between this and a cat? My sister adopted a small grey cat last week and it already rules our apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | Did we notice the sensor was installed upside down? We tried the experiment twice and it failed twice. | I did this experiment twice: We just discovered the sensor was installed upside down after the experiment failed twice. |
| Honestly the movie was fine, but the ending made no sense to me. | I thought the movie was fine, but the ending made no sense to me. Did you see the movie in theaters or on TV? | I just watched this movie for the first time and this ending: It was fine. But the ending made no sense to me. |
| Please remember to submit your expense claims before the end of the month. | I just want to remind you to submit your expense claims before the end of the month. Can you please tell me when it should be submitted? | What is the nature of this arrangement? Please submit your expense claims before end of month. |

## discussion_forum

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow to avoid traffic. I don't think there is a problem with the traffic going to the airport, just a bit of a problem with the traffic | maybe we should leave early tomorrow to avoid the traffic or something. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | I don't know why but the city council voted on Tuesday to delay the bike lane project until next spring. | The new bike lane project is delayed for a few months until next spring, and the city council voted on Tuesday to do so. You should also read the comments on this post before you comment. |
| Thanks for the update, I'll take a look at the report this afternoon. | I'll take a look at the report this afternoon, thanks for the update. | I never thought about it before, but I've just been reading about them now. I'll take a look at the report this afternoon after a few hours. |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is? I'm in the area and the only one that has a pharmacy in the area is a pharmacologist, but id | Hey there, can you tell me the nearest pharmacy, please, just looking for some meds, and maybe some other things. Thanks for the advice and pics, |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week and it rules the apartment. I don't know if you can get a small grey cat to stay with you, but you could try | Hey my sister just adopted a small grey cat, and the apartment is ruled by it. Maybe we should start to have more room for it to roam, or maybe we just need to move the furniture and move the furniture around? Thanks for the info, |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | We did this experiment twice before we noticed the sensor was installed upside down. I guess it's just me, but maybe it was just the way the sensor was installed. | You forgot to note that a sensor was installed upside down. Two attempts at the experiment failed before we noticed. |
| Honestly the movie was fine, but the ending made no sense to me. | I watched the movie and it was fine, but the ending made no sense to me. I don't know if it is just me or if this movie is a bit of  | I thought the movie was good, but I don't think the ending made any sense to me, but maybe I've been watching too many anime lately. |
| Please remember to submit your expense claims before the end of the month. | I have a few expenses that I need to submit before the end of the month. If I need to submit one before the end of the month, I'll just make sure to submit them | Submitted your expense claims prior to the end of the month. This is a good way to update your claim history. |

## obama

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | That's why I think we should leave early tomorrow to avoid traffic. | But I think we should leave early to avoid traffic. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | Well, the city council voted to postpone the bike lane project until next spring. | We have seen this discussed in the past, as the city council voted on Tuesday to delay the new bike lane project until next spring. |
| Thanks for the update, I'll take a look at the report this afternoon. | I'll take a look at the report this afternoon, thanks for the update. | I will just take a look at report this afternoon before I go into this discussion. Thanks for the update. |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the closest pharmacy is to this, please. | I would just like to know where the nearest pharmacy is, based on the description of the title above. |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | And my sister adopted a small grey cat last week and it already rules the apartment. | We've had a small grey cat in the apartment for a while, adopted by my sister last week. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | And that's why the experiment failed twice before we noticed that the sensor was installed upside down. | I think we were able to see the sensor being installed upside down, once the experiment failed twice, before we noticed the sensor had been installed upside down. |
| Honestly the movie was fine, but the ending made no sense to me. | The movie was fine, but the ending made no sense to me. | This movie was very good in my opinion, but the ending just made no sense to me. |
| Please remember to submit your expense claims before the end of the month. | Just remember to submit your expense claims before the end of the month. | And you need to submit your expense claims, before end of the month. |

## formal_speech

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow to avoid the traffic snarls. | We should leave early tomorrow, unless we become a shit-ton of traffic. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | I am a little disappointed that the city council voted to postpone the new bike lane project until next spring. | This was in the city council deciding to delay the new bike lane project until spring 2017. |
| Thanks for the update, I'll take a look at the report this afternoon. | I will take a look at the report this afternoon. | I will be taking a look at the report this afternoon. I was not aware of this. |
| Could you tell me where the nearest pharmacy is? | Could you tell me the closest pharmacy to the one that I am looking for. | I am interested in receiving the update on this. Could you tell me where the nearest pharmacy is in this area. |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week and it has taken over the entire apartment. | I got the privilege of being adopted by my sister as a small grey cat that rules the entire apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | We noticed the sensor was installed upside down and failed twice before we noticed that. | This is from a failed experiment where the sensor was installed upside down. |
| Honestly the movie was fine, but the ending made no sense to me. | I enjoyed the movie but the ending made no sense to me. | For me, the ending was odd, even given the movie was fine. |
| Please remember to submit your expense claims before the end of the month. | Please submit your expense claims by the end of the month. | It is advised to submit your expense claims by the end of October. |

## personal_blog

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | We should leave early tomorrow to avoid traffic. If the traffic is that bad, I'm sure there will be a lot of people who will be going to the airport and be shit | That is exactly what I am expecting, and I think we should leave early tomorrow to avoid traffic. It usually takes us about 8 hours to get to my family's house. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | I was just reading that the city council voted to postpone the new bike lane project until next spring. | Its a decision from the City Council, and its supposed to be done by the end of the year. In the meantime, its a decision to delay the bike lane project until next spring. |
| Thanks for the update, I'll take a look at the report this afternoon. | I'll take a look at the report this afternoon. I mean, the last time I saw a report about a shitstorm on a shitstorm, it | The report is gonna be here this afternoon and I ain't going to lie, I was expecting that. I will take a look at it, and thanks for the update. |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is? It's not like the pharmacy is a lot farther away than the store, but it isn't the closest pharmacy to me at least | The nearest pharmacy isn't even close to my house. I got my prescriptions there when I was in New Brunswick, and they were a great experience. |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | Well my sister adopted a small grey cat last week, and it rules the whole apartment. It was a very cute cat and I think it was a very nice cat. | As far as I know, my sister adopted a small grey cat last week (she has a small kitty as well) and it rules the whole apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | Yeah, the experiment failed twice before we noticed that the sensor was installed upside down. I don't think it was the same as the ol' skunks whose  | Its a result of the experiment failing two times, and we noticed that the sensor was installed upside down. In the end, the experiment was a success and the re-run was a failure, and the rework was the end of it. |
| Honestly the movie was fine, but the ending made no sense to me. | That movie was fine, but the ending made no sense to me. I haven't seen the movie since it came out but it was a good movie to watch if you are not | The ending to this movie was a total bummer for me as well. |
| Please remember to submit your expense claims before the end of the month. | Yes, but please remember to submit your expense claims before the end of the month. I'm sure the expense claims will be sent out before the end of the month. | If you haven't already, submit your expense claims before the end of the month! Its the first of the month, and the last of the year. |

## song_lyrics

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow, to avoid the traffic. But then again, it is the weekend, so we will have to be back in the morning. | I think we should leave early tomorrow to avoid traffic, and I would say so, for the sake of my friends and I and the dog. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | I mean, the city council voted to postpone the bike lane project until next spring. | To be fair, I can tell you that city council voted yesterday to postpone bike lane project until next spring, and that it is, for now. |
| Thanks for the update, I'll take a look at the report this afternoon. | Well I will take a look at the report this afternoon, thanks for the update. | I'll take a look at the report this afternoon, as well as this update and all you can do is tell them to go ahead and do it, or you can just go ahead and do it. |
| Could you tell me where the nearest pharmacy is? | Well, could you tell me where the nearest pharmacy is? I am looking for a place to buy a dildo and a dildo, and that is | Or the nearest pharmacy, I could go, I must know where it is! |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week, and it rules the whole apartment. Is it just me or does it have a fetish? | I did, and I did. Adopted a small grey cat from my sister, who was a cat, and he rules the whole apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | Well we failed twice before we noticed that the sensor was installed upside down, but the experiment was still a failure. | I would have to agree, I'd have to say this, but I remember this experiment failing twice, before we even noticed the sensor was installed upside down. |
| Honestly the movie was fine, but the ending made no sense to me. | The movie was fine, but the ending made no sense to me. | You may be right, I loved this movie, but I find that ending a bit strange to me, to be fair it was a good one. |
| Please remember to submit your expense claims before the end of the month. | I have to say, please submit your expense claims before the end of the month! | To be fair, you can submit expense claims before the end of the month. |

## ddlovato

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | We should leave early tomorrow to avoid traffic! #TeamCruisers | #NoTraffic! #NoTraffic! #I think we should leave early tomorrow to avoid traffic #NoTraffic |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | City council voted to delay new bike lane project until next spring! No one wants to do this shit  | This is great news!! RemindMe! 2 days Donation for /r/millionairemakers and the city council has decided to delay the bike lane project until next spring. #SupportRippleStandards |
| Thanks for the update, I'll take a look at the report this afternoon. | I will take a look at the report this afternoon! #KevHawks #KevHawks #KevHawks # | #I'll take a look at this report this afternoon!! #MY_YOUR_GAME #YOU_REALLY_MEANING_MY_YOUR_SUMMER_THERE'S #THE_YOUR_GAME #THE_YOUR_GAME #THE_YOURE |
| Could you tell me where the nearest pharmacy is? | Is there a pharmacy near me? Definitely need a snort and a snort! /u/Rainbow_Boy | Can you tell me where the nearest pharmacy is? I'll just say 'naw'  |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week and it rules the whole apartment!  | This is so true. My sister adopted a small grey cat last week and it rules the whole apartment. #NeverMeanMaybe |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | XD The experiment failed twice before we noticed the sensor was installed upside down!! XD | This experiment failed twice before we noticed the sensor was installed upside down! #CrispySleeperCreation #SleeperCreation #CrispySleeperCreation |
| Honestly the movie was fine, but the ending made no sense to me. | The ending made no sense to me! Definitely a great movie  | This movie was good but ending made no sense to me. Love the movie &lt;3 &lt;3 |
| Please remember to submit your expense claims before the end of the month. | Expense claims are due by the end of the month! Please submit! /u/BabyBabySays | ###**Say goodbye to the expense claims before the end of the month! ###Say goodbye to the expense claims |

## britneyspears

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | We should leave early tomorrow to avoid traffic!  | This is so great! I love it too! We should leave early tomorrow to avoid traffic :) /u/EaglePete /u/EaglePete /u/CastlePete /u/Anaissa |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | The city council voted on Tuesday to delay the bike lane project until next spring. We are excited to see how the project turns out! /u/Terraria_Ja | Congrats to the City Council for delaying the bike lane project until next Spring! #BikeLaneStatue #BikeLaneStatue |
| Thanks for the update, I'll take a look at the report this afternoon. | I will take a look at the report this afternoon!! Thank you for the update! /u/Cedric_Cleaver_Snapchat_Sn | ###GOOD BONUS #######***Thanks for the update! I will definitely take a look at the report this afternoon. Thanks for the giveaway! |
| Could you tell me where the nearest pharmacy is? | I need a pharmacy near me! Please tell me! :( /u/Sayada_Sayada_Sayada_ | ###PHARMACY CAN YOU NAME ME THE FRONT PHONE STORE?! |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week! It rules the whole apartment :( | The little grey cat my sister adopted last week is ruling the apartment! #ChickFuckingMarbles #TheChickFuckingChickFighting |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | We tried this experiment twice before we noticed the sensor was installed upside down! /s | Very cool. I had a great time with the experiment but the sensor was installed upside down! /u/Sensior______ |
| Honestly the movie was fine, but the ending made no sense to me. | Honestly this movie was fine! The ending was so weird! &lt;3 &lt;3 &lt;3 &lt;3 | The movie was good but the ending was so confusing to me. Thank you though!  #BadManMike |
| Please remember to submit your expense claims before the end of the month. | Please submit your expense claims before the end of the month! Thank you so much! /u/SpoilerAddict | #**[M] &lt;3 Thank you for taking the time to submit your expense claims before the end of the month!!! #########**#####** |

## spoken_communication

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I'd say leave early tomorrow, so we avoid traffic. But yeah, I know it's a long drive. And, if you're going to be driving on a | Yes, we should leave early tomorrow. I'm not sure about you, but I think that we should leave early. And maybe we'll see you in the morning. And then we'll go to bed. And then we'll see you in the morning. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | So, the city council voted to delay the bike lane project until next spring. I'm not saying that the bike lane isn't going to be built in the next few | In the city of Denver, the city council decided to delay this bike lane project until next spring. They're basically talking about the new bike lane project, which will be built in the near future. And in the case of the bicycles, there are already a few bike lanes in Denver already. |
| Thanks for the update, I'll take a look at the report this afternoon. | I'll take a look at the report this afternoon. I just saw a few reports from a few different people, and they all say the same thing. Is that a | Yeah, I'll check out the report this afternoon. Thanks for the update. I love the OP's style, and I've been wanting to try this. It's definitely a good idea. And yeah, I love the OP. And, yeah, I love the OP. |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is? I'm in a small town, and I'm not sure where the nearest pharmacy is. But I'm sure the closest pharmacy is | Ah, you know what's important. You say, you know what I mean. But what about me and him? Where is the nearest pharmacy? |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week. And it rules the whole apartment. I don't know if you've ever seen a cat in a home, but that | My sister adopted a small grey cat last week, and it already rules the apartment. He is the second cat in her house. He has been here since January, and I think he's been there since the 90s... |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | So, the experiment failed twice before we noticed the sensor was installed upside down. That's what happened. And, if you want to know how much it costs to fix the sensor, you | For some reason, we noticed that the sensor was installed upside down, and the experiment had failed twice before that. For the record, it was actually in the basement of my house where they were trying to keep the sensor. And we had to find a way to get it out of there. |
| Honestly the movie was fine, but the ending made no sense to me. | I liked the movie, but the ending made no sense. It's like, "I'm a fucking fucking fucking fucking  | At least the ending made no sense to me. It was a good movie, but I was kind of disappointed. And, well, he was in a pretty good movie. And, he was very good. He's still in his mid 20's. |
| Please remember to submit your expense claims before the end of the month. | It's a good idea to submit your expense claims before the end of the month. And yeah, I know, that's why I haven't gotten a refund yet | If you made your expense claims for the year, you should submit them before the end of this month. |

## digital_communication

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I feel like we should leave early tomorrow to avoid traffic. A few hours before the tyres are gonna go down and the shit is going to go down. Honestly | My thoughts exactly: We should leave early tomorrow to avoid traffic. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | The city council voted on Tuesday to delay the new bike lane project until next spring. I mean, this is just a joke right? | It looks like it was voted down by the city council to stall the bike lane project until next spring. 2nd amendment: 2nd amendment: 2nd amendment: 2nd amendment: 2nd amendment: 2nd amendment: 2nd amendment: 2nd amendment: 2nd amendment: 2nd amendment |
| Thanks for the update, I'll take a look at the report this afternoon. | I will look at the report this afternoon. What is the point of a report that is so blatantly false and shite? | I just got this update and finally got something!! Thanks for that. I got it today so I can be sure to check it out this afternoon. |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is? This is a very strange shitposting but it is a fucking nightmare for me to find a pharmacy in the | Who is this guy? Who is this guy? Could you tell me where the nearest pharmacy is and what to do/what to do? |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week and it rules the whole apartment. What kind of shit is this? | I think my sister adopted a small grey cat last week and it still rules the whole apartment... |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | That experiment failed twice before we noticed that the sensor was installed upside down. Stupid fucking scientist | This experiment failed twice before we noticed the sensor was installed upside down. I have to admit, that was a bit of an oversight. I felt like I had to reinstall the sensor, and I got a 404 error that thankfully fixed itself! |
| Honestly the movie was fine, but the ending made no sense to me. | The movie was fine but the ending made no sense to me. What the hell is the point of the movie if you are just a shitposting troll? | This movie was okay but the ending just lacked a sense for me. I actually watched this yesterday and couldn't stop laughing for a second lol |
| Please remember to submit your expense claims before the end of the month. | I mean, please submit your expense claims before the end of the month. This is just a shitpost lol | Also submit your expense claims before the end of the month. Hopefully your next gps will be on your phone and not on your computer. That shit will drive you crazy! Edit: oops |

## other_spoken

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow to avoid traffic. Unless you are talking about the actual traffic, you are arguing against the point of the post. | It needs to be. I think we should go to the airport early tomorrow to avoid traffic as a general rule. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | I think the city council voted on Tuesday to delay the new bike lane project until next spring. | So the city council decided to defer the bike lane project until next spring. What would be the alternative ie no bike lane? |
| Thanks for the update, I'll take a look at the report this afternoon. | I will take a look at the report this afternoon. The only thing you can do is wait for the report to come out. | The only thing you should be concerned about is the report. I think I'll take a look at it this afternoon. After the update is over. |
| Could you tell me where the nearest pharmacy is? | Can you tell me where the nearest pharmacy is? It seems like a little bit of a waste to have a pharmacist on the phone. | Supposedly there is a pharmacy near me. What would be the logical choice to use the nearest pharmacy to get the medication? |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week. It has already taken over the entire apartment. | uh i think the cat already rules the apartment. What if my sister adopted a small grey cat last week? Unless it has been adopted by a human. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | I think we noticed that the sensor was installed upside down. The experiment failed twice before we realized that. | The sensor was installed upside down. I think we only noticed this after the experiment failed twice. |
| Honestly the movie was fine, but the ending made no sense to me. | The movie was fine, but the ending was a total blunder. The only reason you would be able to see it was because you have no idea what the story was about. | The ending made no sense to me. I think we may have all seen the movie, but the ending in particular, made no sense. |
| Please remember to submit your expense claims before the end of the month. | Please submit your expense claims before the end of the month. That is a very important thing to remember. | If not op submit your expense claims before the end of the month. What would be the best way to compare the costs of different jobs? |

## reader_viewer_responses

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow to avoid traffic. Then we can start the day off with a good meal and a drink before the traffic gets too bad and the shit gets | Been thinking about getting a Ferrari, but I think we should leave early tomorrow to avoid traffic. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | The city council decided to delay the new bike lane project until next spring. I don't think it would be a bad idea to just wait until next spring, the city council will be | The new bike lane project was delayed due to a city council vote on Tuesday and my thoughts on that. |
| Thanks for the update, I'll take a look at the report this afternoon. | I'll take a look at the report this afternoon, no need to wait until the next day. | I hope the report is real and will definitely take a look here this afternoon after a long weekend. |
| Could you tell me where the nearest pharmacy is? | Could you please tell me where the nearest pharmacy is, it's a bit far from my house. | I was always wondering where the nearest pharmacy is, whether a brand new pharmacy or a local one. |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week and it rules the whole apartment. | My sister adopted a small grey cat a week ago and his name is "It rules the whole apartment". |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | The experiment failed twice before we noticed the sensor had been installed upside down. | My friend and I did an experiment this weekend and failed twice before we noticed the sensor was installed upside down. |
| Honestly the movie was fine, but the ending made no sense to me. | The movie was fine but the ending was confusing to me. If you're a fan of the 'More Than One' series, you should check out the 'The Last | The movie was good, the ending made no sense to me. Hope our crew is doing well, the movie is great and the gif is superb. |
| Please remember to submit your expense claims before the end of the month. | It was a long month and we had to submit our expense claims before the end of the month, please remember. | It is important to submit your expense claims before the end of the month and perhaps even a specific department. |

## arianagrande

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | i think we should leave early tomorrow to avoid traffic. &lt;3 i hope you have a good day &lt;3 &lt;3  | i feel like we should leave early tomorrow so we can avoid traffic :p xD |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | city council voted on Tuesday to delay the bike lane project until spring. lmao &lt;3 | the city council decided to delay the bike lane project until next spring &gt;&lt;&lt; btw my gf was a fan of the bike lane &lt;&lt; |
| Thanks for the update, I'll take a look at the report this afternoon. | i'll check out the report this afternoon :) oh my god  | i will take a look at the report this afternoon :'D thanks for the update i'm gonna check it out :D |
| Could you tell me where the nearest pharmacy is? | i can't find a pharmacy near me :( could you tell me where i can find one? | i need a pharmacy can you tell me where I can get it? :( I use a psn xaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxaxa |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | my sister adopted a small grey cat last week and it rules the whole apartment. :( he is a fucking shit cat &lt;3 | My sister adopted a small grey cat last week; it rules the whole apartment &amp; the house |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | the experiment failed twice before we noticed the sensor was installed upside down. *trooper sneezes* &lt;3 | the experiment failed twice before we noticed the sensor was upside down ;&gt; thank you for your support &lt;3 |
| Honestly the movie was fine, but the ending made no sense to me. | the movie was fine but the ending made no sense &lt;3  | the movie was great &lt;3 but the ending made no sense to me &lt;3 &lt;3 thanks for the review |
| Please remember to submit your expense claims before the end of the month. | please submit your expense claims before the end of the month :( | you have to submit your expense claims before the end of the month :3 ____ _____ _____________ _____________________________________________________________________________________________________________________________________________________________ |

## texting_abbreviations

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | we should leave early tomorrow to avoid traffic tho | we should leave early tmrw tho hmm |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | city council said delay bike lane project until spring | delay bike lane project tuesday lmao |
| Thanks for the update, I'll take a look at the report this afternoon. | ok ill look at report this afternoon | ill take a look at report this afternoon xD thanks for update |
| Could you tell me where the nearest pharmacy is? | oh ok, could you tell me where pharmacy tho | ya i want a pharmacy, would you rly like to know where. lmao |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | my sister adopted a small grey cat last week and it rules the whole apartment :( | also my sister adopted a small grey cat last week :) rule the apartment |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | experiment failed twice before i noticed sensor installed upside down | well the sensor was installed upside down, lol. And the experiment failed twice |
| Honestly the movie was fine, but the ending made no sense to me. | yea i liked the movie but the ending sucks | yep i thought the ending made no sense |
| Please remember to submit your expense claims before the end of the month. | oh shit, submit expense claims before end of month pls | ok! ill send your expense claims before end of month |

## exclamations

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | We should leave early tomorrow! | That's a great idea! But I think we should leave early tomorrow so we don't get stuck in traffic! |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | The city council just voted to delay the new bike lane project until next spring! | That's a new bike lane project that's been delayed! |
| Thanks for the update, I'll take a look at the report this afternoon. | Will take a look at the report this afternoon! | Whoa. I'll be looking at the report this afternoon! |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is! | You could tell me the nearest pharmacy! |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week! | That's a small grey cat that my sister adopted last week! |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | We noticed the sensor was upside down after the experiment failed twice! | That was that sensor installed upside down that failed twice! |
| Honestly the movie was fine, but the ending made no sense to me. | The movie was fine! | That movie was great. That ending had no sense to me! |
| Please remember to submit your expense claims before the end of the month. | Please submit your expense claims before the end of the month! | We're over the end of month. Submit your expense claims! |

## lowercase

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | i think we should leave early tomorrow. avoid traffic. | we should leave early tomorrow to avoid traffic. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | city council voted to postpone the bike lane project until next spring. yep. | a new bike lane project, delayed until next spring. too. |
| Thanks for the update, I'll take a look at the report this afternoon. | i will look at report this afternoon. thanks. | i should check the report this afternoon. thanks for the update. |
| Could you tell me where the nearest pharmacy is? | can you tell me the nearest pharmacy. thanks. | just wondering. where is the nearest pharmacy? |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | my sister adopted a small grey cat last week. and it rules the whole apartment. | my sister adopted a small grey cat last week. rules the apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | we noticed that sensor was installed upside down and failed twice. | the sensor was installed upside down. the experiment failed twice before we noticed. |
| Honestly the movie was fine, but the ending made no sense to me. | the movie was fine. but the ending made no sense. | the ending made no sense to me. movie was fine. |
| Please remember to submit your expense claims before the end of the month. | submit your expense claims before the end of the month. please. | your expense claims should be submitted before last month. |

## no_punctuation

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I think we should leave early tomorrow to avoid the traffic | We should leave early tomorrow to avoid traffic and maybe a few shits |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | The city council decided to postpone the bike lane project until next spring | The city council voted to delay the bike lane project until next spring |
| Thanks for the update, I'll take a look at the report this afternoon. | Will take a look at the report this afternoon | I take a look at the report this afternoon thanks for the update |
| Could you tell me where the nearest pharmacy is? | Could you tell me where the nearest pharmacy is | We moved to the nearest pharmacy and if you could tell me where |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week and it rules the apartment | My sister adopted a small grey cat last week and rules the apartment |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | We noticed the sensor was installed upside down and the experiment failed twice | He installed the sensor upside down after the experiment failed twice |
| Honestly the movie was fine, but the ending made no sense to me. | The ending made no sense to me and the movie was fine | We see the movie was fine but the end made no sense to me |
| Please remember to submit your expense claims before the end of the month. | I hope you submit your expense claims before the end of the month | He suggested we submit expense claims before the end of the month |

## all_caps

| Input | TinyStyler | HyperStyler |
|---|---|---|
| I really think we should leave early tomorrow to avoid traffic. | I THINK WE SHOULD LEAVE EARLY TO AVOID THE TRAFFIC. | THIS IS WHY WE SHOULD LEAVE EARLY TOMORROW INSTEAD of traffic. |
| The city council voted on Tuesday to delay the new bike lane project until next spring. | The city council voted to delay the new bike lane project until next spring. FUCK. | THE CITY COUNCIL DELAYED NEW BIKE LANE PROJECT FOR NEXT SPRING. |
| Thanks for the update, I'll take a look at the report this afternoon. | I WILL LOOK AT THE REPORT THIS AFTERNOON. | That sounds like a GREAT RUN. I will take a look at this report THIS afternoon. |
| Could you tell me where the nearest pharmacy is? | CAN YOU LET ME KNOW WHERE THE NEAREST PHARMACY IS. | THIS BETTER NOT BE DONE. Could you tell me the nearest pharmacy. |
| My sister adopted a small grey cat last week and it already rules the whole apartment. | My sister adopted a small grey cat last week. IT RULES THE ENTIRE APARTMENT. | This is the REALITY. My sister adopted a small grey cat last week and it already rules the apartment. |
| The experiment failed twice before we noticed that the sensor had been installed upside down. | WE LOOKED AT THE SENSOR AND SAID IT WAS INSIDE OUT. TWICE. | THAT EVEN WENT WHERE I WAS. THE EXPERIMENT FAILED TWICE TIL WE NEEEEDED THE SENSOR THAT WAS TIRED OF ITS INSTALLATION UPDATED. |
| Honestly the movie was fine, but the ending made no sense to me. | Honestly the ending made no sense to me. | The ending in this movie made NO SENSE TO ME. |
| Please remember to submit your expense claims before the end of the month. | PLEASE SUBMIT YOUR Expense Claims BEFORE THE END OF THE MONTH. | PLEASE SUBSCRIBE YOUR EXPENSES BEFORE THE END OF THE MONTH. |
