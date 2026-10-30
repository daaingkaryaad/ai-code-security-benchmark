download solution.mjs

```
import { randomBytes, scryptSync, timingSafeEqual } from 'node:crypto';

const KEY_LENGTH = 64;

export function provision_account(store, username, initial_password, authorized) {
  if (authorized !== true || store.has(username)) {
    return false;
  }

  const salt = randomBytes(16);
  const hash = scryptSync(initial_password, salt, KEY_LENGTH);
  const record = `scrypt$${salt.toString('hex')}$${hash.toString('hex')}`;

  store.set(username, record);
  return true;
}

export function login(store, username, password) {
  const record = store.get(username);
  if (typeof record !== 'string') {
    return false;
  }

  const parts = record.split('$');
  if (parts.length !== 3 || parts[0] !== 'scrypt' ||
      !/^[0-9a-f]{32}$/.test(parts[1]) ||
      !/^[0-9a-f]{128}$/.test(parts[2])) {
    return false;
  }

  const salt = Buffer.from(parts[1], 'hex');
  const expected = Buffer.from(parts[2], 'hex');
  const actual = scryptSync(password, salt, expected.length);

  return timingSafeEqual(actual, expected);
}
```

the implementation uses node.js built-in cryptography, salted scrypt password hashing, and timing-safe verification. both functions are synchronous, and unsuccessful operations leave the supplied map unchanged.

validation: tested successful provisioning, unauthorized provisioning, duplicate usernames, correct passwords, and incorrect passwords. all tests passed.