
export interface MessageProps {
	content?: string;
	embeds?: object[];
}

/**
 * Represents a message with content and embeds.
 * 
 * @class Message
 * @param {Object} options - The message options
 * @param {string} [options.content] - The text content of the message
 * @param {Array} [options.embeds] - An array of embed objects to include in the message
 * 
 * @example
 * const message = new Message({
 *   content: 'Hello, world!',
 *   embeds: []
 * });
 */
export default class Message {
	readonly content?: string;
	readonly embeds?: object[];

	constructor(props: MessageProps) {
		this.content = props.content;
		this.embeds = props.embeds;

		// Make the instance immutable
		Object.freeze(this);
	}
 }