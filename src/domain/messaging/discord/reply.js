

export async function reply(interaction, message) {
	await interaction.reply({
		content: message.content,
		embeds: message.embeds
	});
}