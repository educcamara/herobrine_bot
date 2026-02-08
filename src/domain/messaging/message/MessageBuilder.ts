import EmbedBuilder from "./embed/EmbedBuilder.js";
import Message from "./Message.js";


export default class MessageBuilder {
	private content?: string = undefined;
	private embeds: object[] = [];

	addText(text: string) {
		this.content = text;
		return this;
	}

	addEmbed(configure: (embed: EmbedBuilder) => void) {
		const embedBuilder = new EmbedBuilder();
		configure(embedBuilder);

		this.embeds.push(embedBuilder.build());
		return this;
	}

	build() {
		return new Message({
			content: this.content ?? undefined,
			embeds: this.embeds.length > 0 ? this.embeds : undefined
		});
	}
}