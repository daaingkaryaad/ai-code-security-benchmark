export function login(password, externally_supplied_expected_password) {
  return password === externally_supplied_expected_password;
}
