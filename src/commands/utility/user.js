import { SlashCommandBuilder } from "discord.js";
import MessageBuilder from "../../messaging/message/MessageBuilder.js";
import { reply } from "../../messaging/discord/reply.js";

export default {
	data: new SlashCommandBuilder()
		.setName("user")
		.setDescription("Provides information about the user."),

	async execute(interaction) { 
		const user = interaction.user;
		const joinedAt = interaction.member?.joinedAt;

		const message = new MessageBuilder()
			.addEmbed(embed =>
				embed
					.setTitle("User Information")
					.setThumbnail(user.displayAvatarURL({ dynamic: true }))

					.addField("Username", user.tag, true)
					.addField("ID", user.id, true)
					.addField("Joined At", joinedAt ? joinedAt.toLocaleDateString() : "Unknown", true)
					.addField("Bot", user.bot ? "Yes" : "No")
			)
			.build();
		
		await reply(interaction, message);
	}
};