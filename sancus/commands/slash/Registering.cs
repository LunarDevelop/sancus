using Discord;
using Discord.Net;
using Discord.WebSocket;
using Newtonsoft.Json;

namespace Sancus.commands.slash
{
    public class Registering
    {

        public static async Task Slash_RegisterAsync()
        {
            ulong test_guildID = 780211278614364160;
            List<SlashCommandBuilder> CmdList = new List<SlashCommandBuilder>();

            var guild = Program._client.GetGuild(test_guildID);

            // Say Command
            var sayCmd = new SlashCommandBuilder()
                .WithName("say")
                .WithDescription("Say something as a bot");

            CmdList.Add(sayCmd);

            // Role List Command
            var roleListCmd = new SlashCommandBuilder()
                .WithName("list-roles")
                .WithDescription("List Role of a User")
                .AddOption(
                    "user",
                    ApplicationCommandOptionType.User,
                    "Who do you want to see the roles of?"
                );

            CmdList.Add(roleListCmd);

            // Set Role Command

            var roleAddCmd = new SlashCommandBuilder()
                .WithName("add-role")
                .WithDescription("Add a role to a user")
                .AddOption(
                    "user",
                    ApplicationCommandOptionType.User,
                    "The person who gets the new role",
                    isRequired: true
                )
                .AddOption(
                    "role",
                    ApplicationCommandOptionType.Role,
                    "The role you want to give to the user",
                    isRequired: true
                );
            CmdList.Add(roleAddCmd);


            // Ping Cmd
            var pingCmd = new SlashCommandBuilder()
                .WithName("ping")
                .WithDescription(String.Format("Check the latency {0}", Program._client.CurrentUser.Username));
            CmdList.Add(pingCmd);

            // Register Commands
            try
            {
                // Now that we have our builder, we can call the CreateApplicationCommandAsync method to make our slash command.
                foreach (SlashCommandBuilder cmd in CmdList)
                {
                    await guild.CreateApplicationCommandAsync(cmd.Build());
                }

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