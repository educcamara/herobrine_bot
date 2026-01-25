import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

import {
	Client,
	Events,
	GatewayIntentBits,
	MessageFlags
} from "discord.js";

import CommandHandler from "./handlers/command-handler.js";
import logger from "./infra/logger.js";

// Setup Paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Client
const client = new Client({
	intents: [GatewayIntentBits.Guilds]
});

// Command Handler
const commandsPath = path.join(__dirname, "commands");
const commandHandler = new CommandHandler(
	pathToFileURL(commandsPath)
);

await commandHandler.load();

// Events

client.once(Events.ClientReady, readyClient => {
	logger.info(`Logged in as ${readyClient.user.tag}`);
});

client.on(Events.InteractionCreate, async interaction => {
	if (!interaction.isChatInputCommand()) {
		logger.info(`Ignoring ${interaction.type} interaction`);
		return;
	}

	try {
		await commandHandler.execute(interaction);
	} catch (error) {
		logger.error(error, "Command execution failed");

		if (!interaction.replied && !interaction.deferred) {
			await interaction.reply({
				content: "Erro ao executar o comando",
				flags: MessageFlags.Ephemeral // only visible to the user
			});
		}
	}
});

export default client;