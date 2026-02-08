
export default class EmbedBuilder {
  #embed = {};
  #fields = [];

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

  setThumbnail(url) {
    this.#embed.thumbnail = { url };
    return this;
  }

  setColor(color) {
    this.#embed.color = color;
    return this;
  }

  setFooter(text) {
    this.#embed.footer = { text };
    return this;
  }

  addField(name, value, inline = false) {
    this.#fields.push({ name, value, inline });
    return this;
  }

  build() {
    if (this.#fields.length > 0) {
      this.#embed.fields = this.#fields;
    }

    return structuredClone(this.#embed);
  }
}