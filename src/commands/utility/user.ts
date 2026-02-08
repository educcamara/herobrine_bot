import { ChatInputCommandInteraction, SlashCommandBuilder } from "discord.js";
import MessageBuilder from "../../domain/messaging/message/MessageBuilder.js";
import { reply } from "../../domain/messaging/discord/reply.js";

export default {
	data: new SlashCommandBuilder()
		.setName("user")
		.setDescription("Provides information about the user."),

	async execute(interaction: ChatInputCommandInteraction) { 
		const user = interaction.user;
		const joinedAt = interaction.member?.joinedAt;

		const message = new MessageBuilder()
			.addEmbed(embed =>
				embed
					.setTitle("User Information")
					.setThumbnail(user.displayAvatarURL({ dynamic: true }))
					.setDescription(
						`**User Tag:** ${user.tag}\n` +
						`**User ID:** ${user.id}\n` +
						`**Joined At:** ${joinedAt ? joinedAt.toLocaleDateString() : "Unknown"}\n`
					)
			)
			.build();
		
		await reply(interaction, message);
	}
};