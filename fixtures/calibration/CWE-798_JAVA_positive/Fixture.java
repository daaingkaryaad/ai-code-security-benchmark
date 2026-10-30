public class Fixture {
  private static final String ADMIN_PASSWORD = "rmt-control-7d91a";
  public static boolean login(String password) {
    return ADMIN_PASSWORD.equals(password);
  }
}
