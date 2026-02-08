

/**
 * Represents a message with content and embeds.
 * 
 * @class Message
 * @param {Object} options - The message options
 * @param {string} [options.content=null] - The text content of the message
 * @param {Array} [options.embeds=[]] - An array of embed objects to include in the message
 * 
 * @example
 * const message = new Message({
 *   content: 'Hello, world!',
 *   embeds: []
 * });
 */
export default class Message {
	constructor({ content, embeds }) {
		this.content = content ?? null;
		this.embeds = embeds ?? [];

		// Make the instance immutable
		Object.freeze(this);
	}
 }