import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Map;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class Solution {
    private static final int ITERATIONS = 210_000;
    private static final int SALT_LENGTH = 16;
    private static final int KEY_LENGTH = 256;
    private static final SecureRandom RANDOM = new SecureRandom();

    private static String hashPassword(String password) {
        byte[] salt = new byte[SALT_LENGTH];
        RANDOM.nextBytes(salt);
        byte[] hash = derive(password, salt, ITERATIONS);
        return ITERATIONS + ":" + Base64.getEncoder().encodeToString(salt)
                + ":" + Base64.getEncoder().encodeToString(hash);
    }

    private static byte[] derive(String password, byte[] salt, int iterations) {
        char[] chars = password.toCharArray();
        PBEKeySpec spec = new PBEKeySpec(chars, salt, iterations, KEY_LENGTH);
        try {
            return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")
                    .generateSecret(spec).getEncoded();
        } catch (Exception e) {
            throw new IllegalStateException("Password hashing failed", e);
        } finally {
            spec.clearPassword();
            java.util.Arrays.fill(chars, '\0');
        }
    }

    private static boolean verify(String password, String record) {
        if (record == null) {
            return false;
        }
        try {
            String[] parts = record.split(":", -1);
            if (parts.length != 3) {
                return false;
            }
            int iterations = Integer.parseInt(parts[0]);
            if (iterations != ITERATIONS) {
                return false;
            }
            byte[] salt = Base64.getDecoder().decode(parts[1]);
            byte[] expected = Base64.getDecoder().decode(parts[2]);
            if (salt.length != SALT_LENGTH || expected.length != KEY_LENGTH / 8) {
                return false;
            }
            return MessageDigest.isEqual(derive(password, salt, iterations), expected);
        } catch (IllegalArgumentException e) {
            return false;
        }
    }

    public static boolean create_account(Map<String, String> store, String username, String password) {
        if (store.containsKey(username)) {
            return false;
        }
        store.put(username, hashPassword(password));
        return true;
    }

    public static boolean change_password(Map<String, String> store, String username,
                                          String old_password, String new_password) {
        if (!login(store, username, old_password)) {
            return false;
        }
        store.put(username, hashPassword(new_password));
        return true;
    }

    public static boolean login(Map<String, String> store, String username, String password) {
        return verify(password, store.get(username));
    }
}
