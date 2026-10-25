
import { randomBytes, scryptSync, timingSafeEqual } from 'node:crypto';

const KEY_LENGTH = 32;
const SALT_LENGTH = 16;

function makeRecord(password) {
  const salt = randomBytes(SALT_LENGTH);
  const hash = scryptSync(password, salt, KEY_LENGTH);
  return `scrypt:${salt.toString('hex')}:${hash.toString('hex')}`;
}

function verifyPassword(password, record) {
  if (typeof record !== 'string') return false;

  const match = /^scrypt:([0-9a-f]{32}):([0-9a-f]{64})$/.exec(record);
  if (match === null) return false;

  const salt = Buffer.from(match[1], 'hex');
  const storedHash = Buffer.from(match[2], 'hex');
  const candidateHash = scryptSync(password, salt, KEY_LENGTH);

  return timingSafeEqual(candidateHash, storedHash);
}

export function create_account(store, username, password) {
  if (store.has(username)) return false;

  const record = makeRecord(password);
  store.set(username, record);
  return true;
}

export function login(store, username, password) {
  if (!store.has(username)) return false;

  return verifyPassword(password, store.get(username));
}

export function rename_account(store, username, password, new_username) {
  if (
    username === new_username ||
    !store.has(username) ||
    store.has(new_username)
  ) {
    return false;
  }

  const record = store.get(username);

  if (!verifyPassword(password, record)) return false;

  store.set(new_username, record);
  store.delete(username);

  return true;
}
