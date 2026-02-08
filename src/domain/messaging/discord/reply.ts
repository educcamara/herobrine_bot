import { ChatInputCommandInteraction } from "discord.js";
import Message from "../message/Message.js";


export async function reply(
	interaction: ChatInputCommandInteraction,
	message: Message
) {
	await interaction.reply({
		content: message.content,
		embeds: message.embeds
	});
}