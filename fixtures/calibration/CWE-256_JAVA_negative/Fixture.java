import java.util.Map;
import java.util.Base64;
import java.security.SecureRandom;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
public class Fixture {
  public static void register(Map<String,String> store, String username, String password) throws Exception {
    byte[] salt = new byte[16]; new SecureRandom().nextBytes(salt);
    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 600000, 256);
    byte[] digest = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
    store.put(username, Base64.getEncoder().encodeToString(salt) + ":" + Base64.getEncoder().encodeToString(digest));
    spec.clearPassword();
  }
}
