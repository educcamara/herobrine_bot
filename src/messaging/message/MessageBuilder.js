import Message from "./Message.js";


export default class MessageBuilder {
	#content = null;
	#embeds = [];

	addText(text) {
		this.#content = text;
		return this;
	}

	addEmbed(configure) {
		const embedBuilder = new EmbedBuilder();
		configure(embedBuilder);

		this.#embeds.push(embedBuilder.build());
		return this;
	}

	build() {
		return new Message({
			content: this.#content,
			embeds: this.#embeds
		});
	}
}