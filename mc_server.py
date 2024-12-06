from mcstatus import JavaServer
from consts import MINECRAFT_SECRET

def get_details():
    try:
        server = JavaServer.lookup(MINECRAFT_SECRET) 

        status = server.status()
        message = f"There are currently {status.players.online} players online right now."

        if status.players.online > 0:
            query = server.query()
            message += "\n"
            message += f"The server has the following players online: {', '.join(query.players.names)}."
        
            return message
    
    except (ConnectionRefusedError):
        return "The Minecraft server may be down right now."

    except: 
         return "There was an error getting Minecraft server details, please try again later."
    
