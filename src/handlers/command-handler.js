import { Collection } from "discord.js";
import { loadCommands } from "../infra/load-commands.js";

export default class CommandHandler {
	#commands = new Collection();

	constructor(commandsRootUrl) {
		this.commandsRootUrl = commandsRootUrl;
	}

	async load() {
		const loaded = await loadCommands(this.commandsRootUrl);

		for (const { module, fileUrl } of loaded) {
			if (!module?.data || !module?.execute) {
				throw new Error(`Invalid command definition in ${fileUrl}`);
			}

			this.#commands.set(module.data.name, module);
		}
	}

	get(name) {
		return this.#commands.get(name);
	}

	async execute(interaction) {
		const command = this.get(interaction.commandName);

		if (!command) {
			console.error(`No command found for ${interaction.commandName}`);
			throw new Error(`Command not found: ${interaction.commandName}`);
		}

		await command.execute(interaction);
	}

	values() {
		return this.#commands.values();
	}

}
