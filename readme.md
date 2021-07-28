#Chess server

Over christmas a bunch of folks in my team made chess bots. One issue they had in the end was actually getting to play
 them against each other. Part of this was to do with them not being able to connect to each other, and another was 
 people building their own engines and not accounting for specific rules.
 
That inspired me to make a server and basic frame work for people to build bots off. Instead of spending time coding up 
the engine and figuring out how to communicate, it's all done already. You can just focus on building a bot to decide what 
move to make. 

I also wanted to learn how to learn about web sockets. Thus, this project uses socketio a whole bunch. 

I'll eventually flesh it out with a HTTP API for folks who don't like the WS approach.
