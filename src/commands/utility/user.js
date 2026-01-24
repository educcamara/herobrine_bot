import { SlashCommandBuilder } from "discord.js";

export default {
	data: new SlashCommandBuilder()
		.setName("user")
		.setDescription("Provides information about the user."),
	async execute(interaction) { 
		const user = interaction.user;
		await interaction.reply(
			`Your username: ${user.username}\nYour ID: ${user.id}\nJoined Discord on: ${interaction.member.joinedAt}` 
		);
	},
};