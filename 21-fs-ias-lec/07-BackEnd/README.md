# IaS Project Group 7: Social Graph Explorer - BackEnd

##Goal
The goal of the project is to represent the social network of BACnet. 
The project was split into two groups: FrontEnd and BackEnd.
We are the BackEnd group, and our main goal is to provide the data needed to represent the graph in a GUI. 
The module "Person.py" and the Json-file "loadedData.json" are interfaces that are provided for the FrontEnd group.

##Interfaces
The following two interfaces are provided:
### Json: loadedData.json
This file is saved in "FrontEnd/socialgraph/static/socialgraph", and it is an interface to save the nodes and edges in the graph. 
First, there is a list of nodes, followed by a list of edges. 

For each node, the attributes of the user are saved. 
The attributes are: gender, birthday, country, town, language, status etc.. We also compute an activity level and an influencer status.

--> MUEMER DAS SO GNAU BESCHRIEBE DA ODER NED?

There are 5 levels of activity: 
* < 10 activities: level 0
* 10-25 activities: level 1
* 25-45 activities: level 2
* 45-70 activities: level 3
* 70-100 activities: level 4
* \> 100 activities: level 5
If a user has more than three followers the influencer status is set to true. This could be changed for big graphs. 
  
For each edge the start and end user-ID are saved.

###Person
This module can be used for changes in the graph while the user is online. The module provides methods to 
change the attributes and methods that handle following and unfollowing. 


--> D LINKS CHAMER USENEH ODER?
## Links:
- Scuttlebut-Guide: https://ssbc.github.io/scuttlebutt-protocol-guide/
- Log File Creation: https://github.com/cn-uofbasel/BACnet/tree/master/20-fs-ias-lec/src/demo
- Feed Controll: https://github.com/cn-uofbasel/BACnet/blob/master/20-fs-ias-lec/groups/14-feedCtrl/project.md
- Scuttlebot: https://scuttlebot.io/docs/basics/install-the-database.html