import { ChatInputCommandInteraction, Collection } from "discord.js";
import { loadCommands } from "../../infrastructure/discord/load-commands.js";
import { Command } from "../../domain/commands/Command.js";

export default class CommandHandler {
	private commands = new Collection<string, Command>();

	constructor(private commandsRootUrl: URL) {}

	async load(): Promise<void> {
		const loaded = await loadCommands(this.commandsRootUrl);

		for (const { module, fileUrl } of loaded) {
			if (!this.isCommand(module)) {
				throw new Error(`Invalid command definition in ${fileUrl}`);
			}

			this.commands.set(module.data.name, module);
		}
	}

	get(name: string): Command | undefined {
		return this.commands.get(name);
	}

	async execute(interaction: ChatInputCommandInteraction): Promise<void> {
		const command = this.get(interaction.commandName);

		if (!command) {
			console.error(`No command found for ${interaction.commandName}`);
			throw new Error(`Command not found: ${interaction.commandName}`);
		}

		await command.execute(interaction);
	}

	values() {
		return this.commands.values();
	}

	private isCommand(module: unknown): module is Command {
		return (
			typeof module === "object" &&
			module !== null &&
			"data" in module &&
			"execute" in module
		);
	}

}
