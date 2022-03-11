using Discord;
using Discord.Net;
using Discord.WebSocket;
using Newtonsoft.Json;
using sancus;
using sancus.commands.slash;
using Sancus.commands.slash;
using System;
using System.IO;

namespace Sancus
{
    public class Program
    {
        public static DiscordSocketClient? _client;

        private Acting act = new Acting();

        public static Task Main(string[] args) => new Program().MainAsync();

        public async Task MainAsync()
        {
            _client = new DiscordSocketClient();

            _client.Log += Log;
            Console.WriteLine(Environment.GetEnvironmentVariable("token"));

            //  You can assign your bot token to a string, and pass that in to connect.
            //  This is, however, insecure, particularly if you plan to have your code hosted in a public repository.
            //var token = "OTUxNDYyMDYyNTMyNDY4Nzc2.Yin0GQ.rrXUYsOLc3eumEhgthh2WEFRUac";

            // Some alternative options would be to keep your token in an Environment Variable or a standalone file.
            var token = Environment.GetEnvironmentVariable("magnet-token");
            // var token = File.ReadAllText("token.txt");
            // var token = JsonConvert.DeserializeObject<AConfigurationClass>(File.ReadAllText("config.json")).Token;

            await _client.LoginAsync(TokenType.Bot, token);
            await _client.StartAsync();

            _client.Ready += Client_Ready;
            _client.SlashCommandExecuted += act.SlashCommandHandler;

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
        }
    }
}