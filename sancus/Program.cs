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
        public static DiscordSocketClient? _client;
        private static SocketGuild test_guild;

        private Acting actSlash = new Acting();
        private ActMsg actMsg = new ActMsg();

        public static SocketGuild Test_guild { get => test_guild; set => test_guild = value; }

        public static Task Main(string[] args) => new Program().MainAsync();

        public async Task MainAsync()
        {
            _client = new DiscordSocketClient();
            var root = Directory.GetCurrentDirectory();
            var dotenv = Path.Combine(root, ".env");
            DotEnv.Load(dotenv);

            Test_guild = _client.GetGuild(780211278614364160);

            _client.Log += Log;
            Console.WriteLine(Environment.GetEnvironmentVariable("token"));

            var token = Environment.GetEnvironmentVariable("magnet-token");

            await _client.LoginAsync(TokenType.Bot, token);
            await _client.StartAsync();

            _client.Ready += Client_Ready;
            _client.SlashCommandExecuted += actSlash.SlashCommandHandler;
            _client.MessageCommandExecuted += actMsg.MessageCommandHandler;


            await _client.SetStatusAsync(UserStatus.DoNotDisturb);
            await _client.SetGameAsync("TESTING SYSTEMS");

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