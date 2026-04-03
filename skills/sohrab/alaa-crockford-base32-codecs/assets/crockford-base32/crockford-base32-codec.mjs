/**
 * Cross-runtime JavaScript reference implementation for the pure lowercase
 * Crockford Base32 codec bundle owned by `alaa-crockford-base32-codecs`.
 *
 * Integer strategy:
 * - positive integers encode as minimal unsigned Crockford Base32 digits
 * - negative integers encode as `-` plus the minimal unsigned magnitude
 * - zero always encodes as `0`
 */
const ALPHABET = '0123456789abcdefghjkmnpqrstvwxyz';

class CrockfordBase32Codec {
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
   * Encode one signed integer using the module's sign-plus-magnitude strategy.
   *
   * @param {bigint | number | string} value
   * @returns {string}
   */
  static encodeInt(value) {
    const integer = this.toBigInt(value);

    if (integer === 0n) {
      return '0';
    }

    const negative = integer < 0n;
    let magnitude = negative ? -integer : integer;
    let encoded = '';

    while (magnitude > 0n) {
      const remainder = Number(magnitude % 32n);
      encoded = ALPHABET[remainder] + encoded;
      magnitude /= 32n;
    }

    return negative ? `-${encoded}` : encoded;
  }

  /**
   * Decode one signed Crockford Base32 integer into canonical base-10 text.
   *
   * Returning decimal text keeps the JavaScript helper lossless for values
   * outside the safe IEEE-754 number range while staying easy to print from CLIs.
   *
   * @param {string} encoded
   * @returns {string}
   */
  static decodeInt(encoded) {
    const { negative, magnitude } = this.splitSignedEncodedInteger(encoded);
    let value = 0n;

    for (const character of magnitude) {
      const digit = ALPHABET.indexOf(character);

      if (digit === -1) {
        throw new TypeError(`Invalid Crockford Base32 integer character [${character}].`);
      }

      value = (value * 32n) + BigInt(digit);
    }

    if (!negative || value === 0n) {
      return value.toString();
    }

    return `-${value.toString()}`;
  }

  /**
   * Encode one UTF-8 JavaScript string as lowercase Crockford Base32.
   *
   * @param {string} value
   * @returns {string}
   */
  static encodeString(value) {
    return this.encodeBytes(new TextEncoder().encode(value));
  }

  /**
   * Decode one Crockford Base32 payload back into a UTF-8 JavaScript string.
   *
   * @param {string} encoded
   * @returns {string}
   */
  static decodeString(encoded) {
    return new TextDecoder('utf-8', { fatal: true }).decode(this.decodeBytes(encoded));
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
   * Encode one canonical UUIDv7 string as lowercase Crockford Base32.
   *
   * @param {string} uuid
   * @returns {string}
   */
  static encodeUuidV7(uuid) {
    const bytes = this.uuidToBytes(uuid);
    this.assertUuidV7Bytes(bytes);

    return this.encodeBytes(bytes);
  }

  /**
   * Decode one Crockford Base32 UUID payload back into canonical UUIDv7 text.
   *
   * @param {string} encoded
   * @returns {string}
   */
  static decodeUuidV7(encoded) {
    const bytes = this.decodeBytes(encoded);

    if (bytes.length !== 16) {
      throw new TypeError('UUIDv7 payload must decode to exactly 16 bytes.');
    }

    this.assertUuidV7Bytes(bytes);

    return this.bytesToUuid(bytes);
  }

  /**
   * Normalize common Crockford aliases before payload validation.
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
   * Parse the module's signed integer wire format.
   *
   * @param {string} encoded
   * @returns {{ negative: boolean, magnitude: string }}
   */
  static splitSignedEncodedInteger(encoded) {
    if (encoded.length === 0) {
      throw new TypeError('Integer payload cannot be empty.');
    }

    const negative = encoded.startsWith('-');
    const magnitude = this.normalizeEncoded(negative ? encoded.slice(1) : encoded);

    if (magnitude.length === 0) {
      throw new TypeError('Integer payload cannot be empty.');
    }

    if (magnitude.length > 1 && magnitude.startsWith('0')) {
      throw new TypeError('Integer payload must use a minimal Crockford Base32 representation.');
    }

    return { negative, magnitude };
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
   * Coerce integer input into an arbitrary-precision `bigint`.
   *
   * @param {bigint | number | string} value
   * @returns {bigint}
   */
  static toBigInt(value) {
    if (typeof value === 'number' && !Number.isInteger(value)) {
      throw new TypeError('Integer input must not contain a fractional component.');
    }

    return typeof value === 'bigint' ? value : BigInt(value);
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

export { CrockfordBase32Codec };
export default CrockfordBase32Codec;
