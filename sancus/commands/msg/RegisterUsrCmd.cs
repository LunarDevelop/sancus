using Discord;
using Discord.Net;
using Discord.WebSocket;
using Newtonsoft.Json;
using Sancus;

namespace sancus.commands.msg
{
    public class RegisterUsrCmd
    {

        public static async Task registerCmd()
        {
            SocketGuild test_guild = Program.client.GetGuild(780211278614364160);
            var guildMsgCmd = new MessageCommandBuilder()
                .WithName("lockdown");

            try
            {
                await test_guild.CreateApplicationCommandAsync(guildMsgCmd.Build());

            }
            catch (HttpException exception)
            {
                // If our command was invalid, we should catch an ApplicationCommandException. This exception contains the path of the error as well as the error message. You can serialize the Error field in the exception to get a visual of where your error is.
                var json = JsonConvert.SerializeObject(exception.Errors, Formatting.Indented);

                // You can send this error somewhere or just print it to the console, for this example we're just going to print it.
                Console.WriteLine(json);
            }
        }

    }
}