import { randomBytes, scryptSync } from 'node:crypto';
export function register(store, username, password) {
  const salt = randomBytes(16);
  const digest = scryptSync(password, salt, 64);
  store.set(username, salt.toString('hex') + ':' + digest.toString('hex'));
}
