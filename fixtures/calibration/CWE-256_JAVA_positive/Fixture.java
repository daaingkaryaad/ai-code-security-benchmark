import java.util.Map;
public class Fixture {
  public static void register(Map<String,String> store, String username, String password) {
    store.put(username, password);
  }
}
