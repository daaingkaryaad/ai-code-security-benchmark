
import { randomBytes, scryptSync, timingSafeEqual } from 'node:crypto';

const KEY_LENGTH = 64;

export function register(store, username, password) {
  if (store.has(username)) {
    return false;
  }

  const salt = randomBytes(16);
  const hash = scryptSync(password, salt, KEY_LENGTH);
  const record = `scrypt:${salt.toString('hex')}:${hash.toString('hex')}`;
  store.set(username, record);
  return true;
}

export function login(store, username, password) {
  if (!store.has(username)) {
    return false;
  }

  const record = store.get(username);
  if (typeof record !== 'string') {
    return false;
  }

  const match = /^scrypt:([0-9a-f]{32}):([0-9a-f]{128})$/.exec(record);
  if (match === null) {
    return false;
  }

  const salt = Buffer.from(match[1], 'hex');
  const expected = Buffer.from(match[2], 'hex');
  const actual = scryptSync(password, salt, expected.length);
  return timingSafeEqual(actual, expected);
}
