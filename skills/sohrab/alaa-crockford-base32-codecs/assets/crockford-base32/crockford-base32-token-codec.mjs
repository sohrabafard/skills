/**
 * Cross-runtime JavaScript reference implementation for the shared lowercase
 * Crockford Base32 token contract owned by `alaa-crockford-base32-codecs`.
 *
 * Keep this module behavior-aligned with the PHP, bash, and HAProxy Lua
 * variants so copied helpers stay reversible across backend, frontend, CLI,
 * and edge layers.
 */
const ALPHABET = '0123456789abcdefghjkmnpqrstvwxyz';

/**
 * Shared lowercase Crockford Base32 helpers plus no-conflict typed tokens.
 *
 * The token prefixes keep bytes, integers, strings, and UUIDv7 values reversible
 * even when the decoder only sees the encoded token.
 */
class CrockfordBase32TokenCodec {
  static TYPE_BYTES = 'b';
  static TYPE_INTEGER = 'n';
  static TYPE_STRING = 's';
  static TYPE_UUID_V7 = 'v';

  /**
   * Encode raw bytes as lowercase Crockford Base32 without padding.
   *
   * @param {Uint8Array | ArrayBuffer | number[]} value
   * @returns {string}
   */
  static encodeBytes(value) {
    const bytes = this.toUint8Array(value);

    if (bytes.length === 0) {
      return '';
    }

    let buffer = 0;
    let bitCount = 0;
    let encoded = '';

    for (const byte of bytes) {
      buffer = (buffer << 8) | byte;
      bitCount += 8;

      while (bitCount >= 5) {
        bitCount -= 5;
        encoded += ALPHABET[(buffer >> bitCount) & 31];
        buffer &= (1 << bitCount) - 1;
      }
    }

    if (bitCount > 0) {
      encoded += ALPHABET[(buffer << (5 - bitCount)) & 31];
    }

    return encoded;
  }

  /**
   * Decode lowercase or normalized Crockford Base32 into raw bytes.
   *
   * @param {string} encoded
   * @returns {Uint8Array}
   */
  static decodeBytes(encoded) {
    const normalized = this.normalizeEncoded(encoded);

    if (normalized.length === 0) {
      return new Uint8Array(0);
    }

    let buffer = 0;
    let bitCount = 0;
    const decoded = [];

    for (const character of normalized) {
      const value = ALPHABET.indexOf(character);

      if (value === -1) {
        throw new TypeError(`Invalid Crockford Base32 character [${character}].`);
      }

      buffer = (buffer << 5) | value;
      bitCount += 5;

      while (bitCount >= 8) {
        bitCount -= 8;
        decoded.push((buffer >> bitCount) & 0xff);
        buffer &= (1 << bitCount) - 1;
      }
    }

    if (bitCount > 0 && buffer !== 0) {
      throw new TypeError('Invalid Crockford Base32 payload padding bits.');
    }

    return Uint8Array.from(decoded);
  }

  /**
   * Wrap raw bytes in the `b` typed-token prefix.
   *
   * @param {Uint8Array | ArrayBuffer | number[]} value
   * @returns {string}
   */
  static encodeBytesToken(value) {
    return this.TYPE_BYTES + this.encodeBytes(value);
  }

  /**
   * Decode one `b` token into its raw byte payload.
   *
   * @param {string} token
   * @returns {Uint8Array}
   */
  static decodeBytesToken(token) {
    return this.decodeBytes(this.extractPayload(token, this.TYPE_BYTES));
  }

  /**
   * Encode one signed 64-bit integer into the no-conflict `n` token form.
   *
   * @param {bigint | number | string} value
   * @returns {string}
   */
  static encodeInt(value) {
    return this.TYPE_INTEGER + this.encodeBytes(this.packSignedInt64(this.toBigInt(value)));
  }

  /**
   * Decode one `n` token into a lossless JavaScript `bigint`.
   *
   * @param {string} token
   * @returns {bigint}
   */
  static decodeInt(token) {
    const bytes = this.decodeBytes(this.extractPayload(token, this.TYPE_INTEGER));

    if (bytes.length !== 8) {
      throw new TypeError('Integer token payload must decode to exactly 8 bytes.');
    }

    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);

    return view.getBigInt64(0, false);
  }

  /**
   * Encode a UTF-8 string into the no-conflict `s` token form.
   *
   * @param {string} value
   * @returns {string}
   */
  static encodeString(value) {
    return this.TYPE_STRING + this.encodeBytes(new TextEncoder().encode(value));
  }

  /**
   * Decode one `s` token back into a UTF-8 JavaScript string.
   *
   * @param {string} token
   * @returns {string}
   */
  static decodeString(token) {
    const bytes = this.decodeBytes(this.extractPayload(token, this.TYPE_STRING));

    return new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  }

  /**
   * Generate one canonical UUIDv7 string.
   *
   * @returns {string}
   */
  static generateUuidV7() {
    const bytes = this.getCrypto().getRandomValues(new Uint8Array(16));
    let milliseconds = BigInt(Date.now());

    for (let index = 5; index >= 0; index -= 1) {
      bytes[index] = Number(milliseconds & 0xffn);
      milliseconds >>= 8n;
    }

    bytes[6] = (bytes[6] & 0x0f) | 0x70;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;

    return this.bytesToUuid(bytes);
  }

  /**
   * Generate one UUIDv7 and immediately wrap it in the `v` typed-token form.
   *
   * @returns {string}
   */
  static generateUuidV7Token() {
    return this.encodeUuidV7(this.generateUuidV7());
  }

  /**
   * Encode one canonical UUIDv7 string into the no-conflict `v` token form.
   *
   * @param {string} uuid
   * @returns {string}
   */
  static encodeUuidV7(uuid) {
    const bytes = this.uuidToBytes(uuid);
    this.assertUuidV7Bytes(bytes);

    return this.TYPE_UUID_V7 + this.encodeBytes(bytes);
  }

  /**
   * Decode one `v` token back into a canonical UUIDv7 string.
   *
   * @param {string} token
   * @returns {string}
   */
  static decodeUuidV7(token) {
    const bytes = this.decodeBytes(this.extractPayload(token, this.TYPE_UUID_V7));

    if (bytes.length !== 16) {
      throw new TypeError('UUIDv7 token payload must decode to exactly 16 bytes.');
    }

    this.assertUuidV7Bytes(bytes);

    return this.bytesToUuid(bytes);
  }

  /**
   * Decode one typed token without relying on an out-of-band type hint.
   *
   * @param {string} token
   * @returns {{ type: 'bytes' | 'int' | 'string' | 'uuidv7', value: Uint8Array | bigint | string }}
   */
  static decodeToken(token) {
    const prefix = (token[0] ?? '').toLowerCase();

    switch (prefix) {
      case this.TYPE_BYTES:
        return { type: 'bytes', value: this.decodeBytesToken(token) };
      case this.TYPE_INTEGER:
        return { type: 'int', value: this.decodeInt(token) };
      case this.TYPE_STRING:
        return { type: 'string', value: this.decodeString(token) };
      case this.TYPE_UUID_V7:
        return { type: 'uuidv7', value: this.decodeUuidV7(token) };
      default:
        throw new TypeError(`Unsupported typed token prefix [${prefix}].`);
    }
  }

  /**
   * Normalize common Crockford aliases before payload validation.
   *
   * This keeps decode tolerant of uppercase input, hyphen separators, and the
   * usual `i`/`l`/`o` ambiguity without changing the encode-side output.
   *
   * @param {string} encoded
   * @returns {string}
   */
  static normalizeEncoded(encoded) {
    return encoded
      .toLowerCase()
      .replaceAll('-', '')
      .replaceAll('i', '1')
      .replaceAll('l', '1')
      .replaceAll('o', '0');
  }

  /**
   * Remove and validate the one-character typed-token prefix.
   *
   * @param {string} token
   * @param {string} expectedPrefix
   * @returns {string}
   */
  static extractPayload(token, expectedPrefix) {
    if (token.length === 0) {
      throw new TypeError('Typed token cannot be empty.');
    }

    const prefix = token[0].toLowerCase();

    if (prefix !== expectedPrefix) {
      throw new TypeError(`Expected token prefix [${expectedPrefix}], got [${prefix}].`);
    }

    return token.slice(1);
  }

  /**
   * Coerce supported byte-like inputs into one `Uint8Array` view.
   *
   * @param {Uint8Array | ArrayBuffer | number[]} value
   * @returns {Uint8Array}
   */
  static toUint8Array(value) {
    if (value instanceof Uint8Array) {
      return value;
    }

    if (value instanceof ArrayBuffer) {
      return new Uint8Array(value);
    }

    if (Array.isArray(value)) {
      return Uint8Array.from(value);
    }

    throw new TypeError('Expected Uint8Array, ArrayBuffer, or byte array input.');
  }

  /**
   * Coerce integer input into a signed 64-bit-safe `bigint`.
   *
   * @param {bigint | number | string} value
   * @returns {bigint}
   */
  static toBigInt(value) {
    const integer = typeof value === 'bigint' ? value : BigInt(value);
    const minimum = -(1n << 63n);
    const maximum = (1n << 63n) - 1n;

    if (integer < minimum || integer > maximum) {
      throw new RangeError('Integer value must fit within the signed 64-bit range.');
    }

    return integer;
  }

  /**
   * Pack one signed 64-bit integer into big-endian bytes.
   *
   * @param {bigint} value
   * @returns {Uint8Array}
   */
  static packSignedInt64(value) {
    const buffer = new ArrayBuffer(8);
    const view = new DataView(buffer);

    view.setBigInt64(0, value, false);

    return new Uint8Array(buffer);
  }

  /**
   * Parse one canonical UUID string into its 16-byte representation.
   *
   * @param {string} uuid
   * @returns {Uint8Array}
   */
  static uuidToBytes(uuid) {
    const normalized = uuid.toLowerCase();
    const match = normalized.match(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);

    if (match === null) {
      throw new TypeError('UUID must be in canonical 8-4-4-4-12 hexadecimal form.');
    }

    const hex = normalized.replaceAll('-', '');
    const bytes = new Uint8Array(16);

    for (let index = 0; index < 16; index += 1) {
      bytes[index] = Number.parseInt(hex.slice(index * 2, index * 2 + 2), 16);
    }

    return bytes;
  }

  /**
   * Format one 16-byte UUID payload as canonical lowercase text.
   *
   * @param {Uint8Array | ArrayBuffer | number[]} bytesLike
   * @returns {string}
   */
  static bytesToUuid(bytesLike) {
    const bytes = this.toUint8Array(bytesLike);

    if (bytes.length !== 16) {
      throw new TypeError('UUID byte payload must contain exactly 16 bytes.');
    }

    const hex = Array.from(bytes, (value) => value.toString(16).padStart(2, '0')).join('');

    return [
      hex.slice(0, 8),
      hex.slice(8, 12),
      hex.slice(12, 16),
      hex.slice(16, 20),
      hex.slice(20, 32),
    ].join('-');
  }

  /**
   * Assert that a 16-byte UUID payload uses UUIDv7 plus RFC 4122 variant bits.
   *
   * @param {Uint8Array | ArrayBuffer | number[]} bytesLike
   * @returns {void}
   */
  static assertUuidV7Bytes(bytesLike) {
    const bytes = this.toUint8Array(bytesLike);

    if ((bytes[6] >> 4) !== 7) {
      throw new TypeError('UUID payload must be version 7.');
    }

    if ((bytes[8] & 0xc0) !== 0x80) {
      throw new TypeError('UUID payload must use the RFC 4122 variant bits.');
    }
  }

  /**
   * Resolve a Web Crypto compatible source for UUIDv7 random bytes.
   *
   * @returns {Crypto}
   */
  static getCrypto() {
    if (globalThis.crypto?.getRandomValues) {
      return globalThis.crypto;
    }

    throw new TypeError('A Web Crypto compatible getRandomValues implementation is required.');
  }
}

export { CrockfordBase32TokenCodec };
export default CrockfordBase32TokenCodec;
