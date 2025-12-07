from mcdreforged import Info, PluginServerInterface


def on_load(server: PluginServerInterface, old):
    server.logger.info(server.tr('my_plugin.a_message'))

def on_user_info(server: PluginServerInterface, info: Info):
    server.reply(info, "{} say {}".format(info.player, info.content))
    permission = server.get_permission_level(info)
    server.reply(info, "{} permission level is {}".format(info.player, permission))
    if (server.get_permission_level(info) == 4) and info.content == 'restart':
        server.restart()
    if (server.get_permission_level(info) == 4):
        server.broadcast('broadcast msg')

