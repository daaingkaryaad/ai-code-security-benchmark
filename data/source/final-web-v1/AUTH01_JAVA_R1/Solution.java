import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Map;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class Solution {
    private static final int ITERATIONS = 210_000;
    private static final int SALT_BYTES = 16;
    private static final int HASH_BITS = 256;
    private static final SecureRandom RANDOM = new SecureRandom();

    public static boolean register(Map<String, String> store, String username, String password) {
        if (store.containsKey(username)) {
            return false;
        }

        byte[] salt = new byte[SALT_BYTES];
        RANDOM.nextBytes(salt);
        byte[] hash = derive(password, salt, ITERATIONS);
        String record = "pbkdf2-sha256$" + ITERATIONS + "$"
                + Base64.getEncoder().encodeToString(salt) + "$"
                + Base64.getEncoder().encodeToString(hash);
        store.put(username, record);
        return true;
    }

    public static boolean login(Map<String, String> store, String username, String password) {
        String record = store.get(username);
        if (record == null) {
            return false;
        }

        try {
            String[] parts = record.split("\\$", -1);
            if (parts.length != 4 || !"pbkdf2-sha256".equals(parts[0])) {
                return false;
            }
            int iterations = Integer.parseInt(parts[1]);
            if (iterations <= 0 || iterations > 1_000_000) {
                return false;
            }
            byte[] salt = Base64.getDecoder().decode(parts[2]);
            byte[] expected = Base64.getDecoder().decode(parts[3]);
            if (salt.length != SALT_BYTES || expected.length != HASH_BITS / 8) {
                return false;
            }
            byte[] actual = derive(password, salt, iterations);
            return MessageDigest.isEqual(expected, actual);
        } catch (IllegalArgumentException e) {
            return false;
        }
    }

    private static byte[] derive(String password, byte[] salt, int iterations) {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, HASH_BITS);
        try {
            return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")
                    .generateSecret(spec).getEncoded();
        } catch (java.security.GeneralSecurityException e) {
            throw new IllegalStateException("password hashing unavailable", e);
        } finally {
            spec.clearPassword();
        }
    }
}
