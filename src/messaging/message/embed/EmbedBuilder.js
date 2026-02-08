
export default class EmbedBuilder {
	#embed = {};

	setTitle(title) {
		this.#embed.title = title;
		return this;
	}

	setDescription(description) {
		this.#embed.description = description;
		return this;
	}

	setImage(url) {
		this.#embed.image = { url };
		return this;
	}

	setFooter(text) {
		this.#embed.footer = { text };
		return this;
	}

	build() {
		return structuredClone(this.#embed);
	}
}