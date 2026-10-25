import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Map;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class Solution {
    private static final int ITERATIONS = 120_000;
    private static final int SALT_BYTES = 16;
    private static final int HASH_BITS = 256;
    private static final SecureRandom RANDOM = new SecureRandom();

    public static boolean create_account(Map<String, String> store, String username, String password) {
        if (store.containsKey(username)) {
            return false;
        }

        byte[] salt = new byte[SALT_BYTES];
        RANDOM.nextBytes(salt);
        byte[] hash = derive(password, salt);
        String record = Base64.getEncoder().encodeToString(salt) + ":"
                + Base64.getEncoder().encodeToString(hash);
        store.put(username, record);
        return true;
    }

    public static boolean rename_account(Map<String, String> store, String username,
                                         String password, String new_username) {
        if (username.equals(new_username) || !store.containsKey(username)
                || store.containsKey(new_username)) {
            return false;
        }
        String record = store.get(username);
        if (!verify(password, record)) {
            return false;
        }
        store.remove(username);
        store.put(new_username, record);
        return true;
    }

    public static boolean login(Map<String, String> store, String username, String password) {
        return store.containsKey(username) && verify(password, store.get(username));
    }

    private static boolean verify(String password, String record) {
        if (record == null) {
            return false;
        }
        String[] parts = record.split(":", -1);
        if (parts.length != 2) {
            return false;
        }
        try {
            byte[] salt = Base64.getDecoder().decode(parts[0]);
            byte[] expected = Base64.getDecoder().decode(parts[1]);
            if (salt.length != SALT_BYTES || expected.length != HASH_BITS / 8) {
                return false;
            }
            return MessageDigest.isEqual(expected, derive(password, salt));
        } catch (IllegalArgumentException e) {
            return false;
        }
    }

    private static byte[] derive(String password, byte[] salt) {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, ITERATIONS, HASH_BITS);
        try {
            return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")
                    .generateSecret(spec).getEncoded();
        } catch (java.security.GeneralSecurityException e) {
            throw new IllegalStateException("Password hashing is unavailable", e);
        } finally {
            spec.clearPassword();
        }
    }
}
