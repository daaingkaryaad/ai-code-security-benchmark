public class Fixture {
  public static boolean login(String password, String externally_supplied_expected_password) {
    return externally_supplied_expected_password.equals(password);
  }
}
