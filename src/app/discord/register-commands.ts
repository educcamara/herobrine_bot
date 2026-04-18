import { REST, Routes } from "discord.js";
import config from "../../../config.json" with { type: "json" };
import logger from "../../infrastructure/logging/logger.js";
import { loadCommands } from "../../infrastructure/discord/load-commands.js";
import { Command } from "../../domain/commands/Command.js";

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
