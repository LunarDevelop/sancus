using Discord;
using Discord.Net;
using Discord.WebSocket;
using Newtonsoft.Json;
using sancus;
using sancus.commands.slash;
using sancus.commands.msg;
using Sancus.commands.slash;
using System;
using System.IO;

namespace Sancus
{
    public class Program
    {
        public static DiscordSocketClient client;
        public static SocketGuild test_guild;

        private Acting actSlash = new Acting();
        private ActMsg actMsg = new ActMsg();

        public static Task Main(string[] args) => new Program().MainAsync();

        public async Task MainAsync()
        {
            client = new DiscordSocketClient();
            var root = Directory.GetCurrentDirectory();
            var dotenv = Path.Combine(root, ".env");
            DotEnv.Load(dotenv);

            Test_guild = client.GetGuild(780211278614364160);

            client.Log += Log;
            Console.WriteLine(Environment.GetEnvironmentVariable("token"));

            var token = Environment.GetEnvironmentVariable("magnet-token");

            await client.LoginAsync(TokenType.Bot, token);
            await client.StartAsync();

            client.Ready += Client_Ready;
            client.SlashCommandExecuted += actSlash.SlashCommandHandler;
            client.MessageCommandExecuted += actMsg.MessageCommandHandler;


            await client.SetStatusAsync(UserStatus.DoNotDisturb);
            await client.SetGameAsync("TESTING SYSTEMS");

            // Block this task until the program is closed.
            await Task.Delay(-1);
        }

        private Task Log(LogMessage msg)
        {
            Console.WriteLine(msg.ToString());
            return Task.CompletedTask;
        }
        public async Task Client_Ready()
        {
            await Registering.Slash_RegisterAsync();
            await RegisterUsrCmd.registerCmd();
        }
    }
}