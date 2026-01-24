const { Client, Events, GatewayIntentBits } = require('discord.js');
const { token } = require('./config.json');
const { default: logger } = require('./src/logger');

const client = new Client({
	intents: [GatewayIntentBits.Guilds]
});

client.once(Events.ClientReady, (readyClient) => {
	logger.info(`Logged in as ${readyClient.user.tag}`);
});

client.login(token).catch((error) => {
	logger.error('Failed to login:', error);
});