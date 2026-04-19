import { 
	ChatInputCommandInteraction, 
	SlashCommandBuilder,
	SlashCommandOptionsOnlyBuilder
} from "discord.js";

export type CommandData = (
	| SlashCommandBuilder
	| SlashCommandOptionsOnlyBuilder
);

export interface Command {
	data: CommandData;
	execute(interaction: ChatInputCommandInteraction): Promise<void>;
}