
export function profile_update(connection, username, new_email) {
  const statement = connection.prepare(
    'UPDATE profiles SET email = ? WHERE username = ?'
  );
  const result = statement.run(new_email, username);
  return result.changes;
}
