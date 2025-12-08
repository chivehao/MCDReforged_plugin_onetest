from mcdreforged import Info, PluginServerInterface
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/test")
async def test():
    return "Hello, world!"

class ServerStatus(Enum):
    DOWN = 1
    UP = 2
    START_PRE = 3
    STARTING = 4
    
server_status:ServerStatus = ServerStatus.DOWN

def on_server_start_pre(server: PluginServerInterface):
    global server_status
    server_status = ServerStatus.START_PRE
    server.logger.info('update server status to {}'.format(server_status.name))

def on_server_start(server: PluginServerInterface):
    global server_status
    server_status = ServerStatus.STARTING
    server.logger.info('update server status to {}'.format(server_status.name))

def on_server_startup(server: PluginServerInterface):
    global server_status
    server_status = ServerStatus.UP
    server.logger.info('update server status to {}'.format(server_status.name))
    global players
    players = []

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    # if server_return_code != 0:
    #     server.logger.info('Is it a server crash?')
    global server_status
    server_status = ServerStatus.DOWN
    server.logger.info('update server status to {}'.format(server_status.name))

@app.get("/server/status")
async def get_server_status():
    return server_status.name

players = []

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    server.say('Welcome {}'.format(player))
    global players
    if player not in players:
        players.append(player)
        server.logger.info('add {} to players'.format(player))

def on_player_left(server: PluginServerInterface, player: str):
    global players
    if player in players:
        players.remove(player)
        server.logger.info('remove {} from players'.format(player))


@app.get("/server/players")
async def get_server_players():
    global players
    return players
    if server_status == ServerStatus.UP:
        return players
    else:
        return server_status.name

def mount_app(server):
    # save plugin id and fastapi_mcdr instance
    id_ = server.get_self_metadata().id
    fastapi_mcdr = server.get_plugin_instance('fastapi_mcdr')

    # mount app
    fastapi_mcdr.mount(id_, app)

def on_load(server: PluginServerInterface, old):
    server.logger.info(server.tr('my_plugin.a_message'))
    # mount if fastapi_mcdr is ready
    fastapi_mcdr = server.get_plugin_instance('fastapi_mcdr')
    if fastapi_mcdr is not None and fastapi_mcdr.is_ready():
        mount_app(server)

    # register event listener
    server.register_event_listener(
        fastapi_mcdr.COLLECT_EVENT,
        mount_app
    )

def on_unload(server):
    # save plugin id and fastapi_mcdr instance
    id_ = server.get_self_metadata().id
    fastapi_mcdr = server.get_plugin_instance('fastapi_mcdr')

    # unmount app
    fastapi_mcdr.unmount(id_)

# def on_user_info(server: PluginServerInterface, info: Info):
#     server.reply(info, "{} say {}".format(info.player, info.content))
#     permission = server.get_permission_level(info)
#     server.reply(info, "{} permission level is {}".format(info.player, permission))
#     if (server.get_permission_level(info) == 4) and info.content == 'restart':
#         server.restart()
#     if (server.get_permission_level(info) == 4):
#         server.broadcast('broadcast msg')

