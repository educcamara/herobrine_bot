import { ChatInputCommandInteraction, GuildMember, SlashCommandBuilder } from "discord.js";

import { reply } from "../../domain/messaging/discord/reply.js";
import MessageBuilder from "../../domain/messaging/message/MessageBuilder.js";
import { Command } from "../../domain/commands/Command.js";

const command: Command = {
	data: new SlashCommandBuilder()
		.setName("user")
		.setDescription("Provides information about the user."),

	async execute(interaction: ChatInputCommandInteraction) { 
		const user = interaction.user;
		let joinedAt: Date | null = null;

		if (interaction.member instanceof GuildMember) {
			joinedAt = interaction.member.joinedAt;
		}

		const message = new MessageBuilder()
			.addEmbed(embed =>
				embed
					.setTitle("User Information")
					.setThumbnail(user.displayAvatarURL())
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

export default command;