from mcdreforged import Info, PluginServerInterface
from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
async def test():
    return "Hello, world!"

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

def on_user_info(server: PluginServerInterface, info: Info):
    server.reply(info, "{} say {}".format(info.player, info.content))
    permission = server.get_permission_level(info)
    server.reply(info, "{} permission level is {}".format(info.player, permission))
    if (server.get_permission_level(info) == 4) and info.content == 'restart':
        server.restart()
    if (server.get_permission_level(info) == 4):
        server.broadcast('broadcast msg')

