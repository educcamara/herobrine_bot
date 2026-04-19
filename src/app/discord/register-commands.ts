import { REST, Routes } from "discord.js";
import logger from "../../infrastructure/logging/logger.js";
import { loadCommands } from "../../infrastructure/discord/load-commands.js";
import { Command } from "../../domain/commands/Command.js";
import config from "../../config/env.js";

function isCommand(module: unknown): module is Command {
	return (
		typeof module === "object" &&
		module !== null &&
		"data" in module &&
		"execute" in module
	)
}

// Setup Paths
const commandsRoot = new URL("../../commands", import.meta.url);
const loaded = await loadCommands(commandsRoot);

const commands = loaded
  .filter(
    (item): item is { module: Command; fileUrl: URL } => {
      if (!isCommand(item.module)) {
        logger.warn(`Skipping command at ${item.fileUrl}: invalid command format`);
        return false;
      }
      return true;
    }
  )
  .map(({ module }) => module.data.toJSON());

// REST Client
const rest = new REST({ version: "10" }).setToken(config.discord.token);

// Deploy Commands
try {
	logger.info(`Registering ${commands.length} commands...`);

	const isProduction = config.nodeEnv === "production";
	
	if (isProduction) {
		logger.info("Deploying commands globally...");
		const route = Routes.applicationCommands(config.discord.clientId);
		await rest.put(route, { body: commands });

	} else {
		logger.info("Deploying commands to guild...");
		if (!config.discord.guildId) {
			throw new Error("Guild ID is required for development deployment");
		}
		const route = Routes.applicationGuildCommands(config.discord.clientId, config.discord.guildId);
		await rest.put(route, { body: commands });
		
	}

	logger.info("Commands registered successfully.");
} catch (error) {
	logger.error(`Failed to register commands: ${error instanceof Error ? error.message : String(error)}`);
}
