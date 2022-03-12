using Discord;
using Discord.WebSocket;
using Sancus;

namespace sancus.commands.slash
{
    public class Acting
    {
        public async Task SlashCommandHandler(SocketSlashCommand command)
        {

            // Let's add a switch statement for the command name so we can handle multiple commands in one event.
            switch (command.Data.Name)
            {
                case "list-roles":
                    await HandleListRoleCommand(command);
                    break;
                case "add-role":
                    await HandleAddRoleCommand(command);
                    break;

                case "ping":
                    await HandlePingCommand(command);
                    break;
            }
        }

        private async Task HandleListRoleCommand(SocketSlashCommand command)
        {
            SocketGuildUser guildUser;
            // Set the guildUser parameter
            if (command.Data.Options.Count == 0)
            {
                guildUser = (SocketGuildUser)command.User;
            }
            else
            {
                guildUser = (SocketGuildUser)command.Data.Options.First().Value;
            }

            // Set the role list up, removing the @everyone role
            var roleList = string.Join(",\n", guildUser.Roles.Where(x => !x.IsEveryone).Select(x => x.Mention));

            var embedBuiler = new EmbedBuilder()
                .WithAuthor(guildUser.ToString(), guildUser.GetAvatarUrl() ?? guildUser.GetDefaultAvatarUrl())
                .WithTitle("Roles")
                .WithDescription(roleList)
                .WithColor(Color.Green)
                .WithCurrentTimestamp();

            // Now, Let's respond with the embed.
            await command.RespondAsync(embed: embedBuiler.Build(), ephemeral: true);
        }

        private async Task HandleAddRoleCommand(SocketSlashCommand command)
        {
            // We need to extract the user parameter from the command. since we only have one option and it's required, we can just use the first option.
            var guildUser = (SocketGuildUser)command.Data.Options.First().Value;
            var guildRole = (SocketRole)command.Data.Options.Last().Value;

            await guildUser.AddRoleAsync(guildRole);

            // We remove the everyone role and select the mention of each role.
            var message = String.Format("{0} has been given the role of {1}", guildUser.DisplayName, guildRole.Name);

            var embedBuiler = new EmbedBuilder()
                .WithAuthor(guildUser.ToString(), guildUser.GetAvatarUrl() ?? guildUser.GetDefaultAvatarUrl())
                .WithTitle("Roles")
                .WithDescription(message)
                .WithColor(Color.Purple)
                .WithCurrentTimestamp();

            // Now, Let's respond with the embed.
            await command.RespondAsync(embed: embedBuiler.Build(), ephemeral: true);
        }

        private async Task HandlePingCommand(SocketSlashCommand command)
        {

            var message = String.Format("Latency: `{0}ms`", Program.client.Latency);

            var embedBuiler = new EmbedBuilder()
                .WithTitle("Ping Checker")
                .WithDescription(message)
                .WithColor(Color.Purple)
                .WithCurrentTimestamp();

            // Now, Let's respond with the embed.
            await command.RespondAsync(embed: embedBuiler.Build());
        }
    }
}