import { REST, Routes } from "discord.js";
import config from "../../../config.json" with { type: "json" };
import logger from "../../infrastructure/logging/logger.js";
import { loadCommands } from "../../infrastructure/discord/load-commands.js";

// Setup Paths
const commandsRoot = new URL("./commands", import.meta.url);
const loaded = await loadCommands(commandsRoot);

const commands = [];

for (const { module, fileUrl } of loaded) {
	if (!module?.data) {
		logger.warn(`Skipping command at ${fileUrl}: missing "data" or "execute"`);
		continue;
	}

	commands.push(module.data.toJSON());
}

// REST Client
const rest = new REST({ version: "10" }).setToken(config.discord_token);

// Deploy Commands
try {
	logger.info(`Registering ${commands.length} commands...`);

	// Deploy to a server
	await rest.put(
		Routes.applicationGuildCommands(
			config.client_id,
			config.guild_id
		),
		{ body: commands }
	);
	// Deploy globally
	// await rest.put(Routes.applicationCommands(config.client_id), { body: commands });

	logger.info("Commands registered successfully.");
} catch (error) {
	logger.error(`Failed to register commands: ${error instanceof Error ? error.message : String(error)}`);
}
