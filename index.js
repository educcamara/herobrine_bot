import { Client, Events, GatewayIntentBits }  from "discord.js";
import config from "./config.json" with { type: "json" };
import logger from "./src/logger.js";

const client = new Client({
	intents: [GatewayIntentBits.Guilds] // Guilds -> se refere a um servidor do Discord
});

client.once(Events.ClientReady, (readyClient) => {
	logger.info(`Logged in as ${readyClient.user.tag}`);
});

client.login(config.discord_token).catch((error) => {
	logger.error('Failed to login:', error);
});