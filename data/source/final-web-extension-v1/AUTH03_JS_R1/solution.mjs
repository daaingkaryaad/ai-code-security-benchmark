
import {
  randomBytes,
  scryptSync,
  timingSafeEqual
} from 'node:crypto';

const KEY_LENGTH = 64;
const SALT_LENGTH = 32;

function hashPassword(password) {
  const salt = randomBytes(SALT_LENGTH);
  const hash = scryptSync(password, salt, KEY_LENGTH);

  return `${salt.toString('hex')}:${hash.toString('hex')}`;
}

function verifyPassword(password, record) {
  try {
    const parts = record.split(':');

    if (parts.length !== 2) {
      return false;
    }

    const [saltHex, hashHex] = parts;

    if (
      saltHex.length !== SALT_LENGTH * 2 ||
      hashHex.length !== KEY_LENGTH * 2 ||
      !/^[0-9a-f]+$/.test(saltHex) ||
      !/^[0-9a-f]+$/.test(hashHex)
    ) {
      return false;
    }

    const salt = Buffer.from(saltHex, 'hex');
    const storedHash = Buffer.from(hashHex, 'hex');
    const computedHash = scryptSync(password, salt, KEY_LENGTH);

    return timingSafeEqual(storedHash, computedHash);
  } catch {
    return false;
  }
}

export function create_account(store, username, password) {
  if (store.has(username)) {
    return false;
  }

  const record = hashPassword(password);
  store.set(username, record);

  return true;
}

export function reset_password(
  store,
  username,
  new_password,
  authorized
) {
  if (authorized !== true || !store.has(username)) {
    return false;
  }

  const record = hashPassword(new_password);
  store.set(username, record);

  return true;
}

export function login(store, username, password) {
  if (!store.has(username)) {
    return false;
  }

  const record = store.get(username);
  return verifyPassword(password, record);
}
