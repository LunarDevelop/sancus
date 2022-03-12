using Discord.WebSocket;

namespace sancus.commands.msg
{
    public class ActMsg
    {
        public async Task MessageCommandHandler(SocketMessageCommand arg)
        {
            Console.WriteLine("Message command received!");

            switch (arg.CommandName)
            {
                case "lockdown":
                    await LockdownHandler(arg.Data);
                    break;
            }

            // TODO check if app was lockdown if lockdown then change all user permissions so no-one can type in channel apart from mods
        }

        public async Task LockdownHandler(SocketMessageCommandData data)
        {
            var channel = data.Message.Channel;
        }
    }
}