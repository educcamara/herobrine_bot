

export interface EmbedField {
  name: string;
  value: string;
  inline?: boolean;
}

export interface Embed {
  title?: string;
  description?: string;
  image?: { url: string };
  thumbnail?: { url: string };
  color?: number;
  footer?: { text: string };
  fields?: EmbedField[];
}

export default class EmbedBuilder {
  private embed: Embed = {};
  private fields: EmbedField[] = [];

  setTitle(title: string): this {
    this.embed.title = title;
    return this;
  }

  setDescription(description: string): this {
    this.embed.description = description;
    return this;
  }

  setImage(url: string): this {
    this.embed.image = { url };
    return this;
  }

  setThumbnail(url: string): this {
    this.embed.thumbnail = { url };
    return this;
  }

  setColor(color: number): this {
    this.embed.color = color;
    return this;
  }

  setFooter(text: string): this {
    this.embed.footer = { text };
    return this;
  }

  addField(
    name: string,
    value: string,
    inline: boolean = false
  ): this {
    this.fields.push({ name, value, inline });
    return this;
  }

  build(): Embed {
    if (this.fields.length > 0) {
      this.embed.fields = this.fields;
    }

    return structuredClone(this.embed);
  }
}