`Solution.java`

```

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.util.Base64;
import java.util.Map;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class Solution {
    private static final int ITERATIONS = 210000;
    private static final int KEY_LENGTH = 256;
    private static final int SALT_LENGTH = 16;
    private static final SecureRandom RANDOM = new SecureRandom();

    private static String hashPassword(String password) {
        byte[] salt = new byte[SALT_LENGTH];
        RANDOM.nextBytes(salt);

        char[] chars = password.toCharArray();
        PBEKeySpec spec = new PBEKeySpec(
            chars, salt, ITERATIONS, KEY_LENGTH
        );

        try {
            SecretKeyFactory factory = SecretKeyFactory.getInstance(
                "PBKDF2WithHmacSHA256"
            );
            byte[] hash = factory.generateSecret(spec).getEncoded();

            return ITERATIONS + ":" +
                Base64.getEncoder().encodeToString(salt) + ":" +
                Base64.getEncoder().encodeToString(hash);
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            throw new IllegalStateException(e);
        } finally {
            spec.clearPassword();
            java.util.Arrays.fill(chars, '\0');
        }
    }

    private static boolean verifyPassword(String password, String record) {
        if (record == null) {
            return false;
        }

        try {
            String[] parts = record.split(":", -1);
            if (parts.length != 3) {
                return false;
            }

            int iterations = Integer.parseInt(parts[0]);
            if (iterations <= 0) {
                return false;
            }

            byte[] salt = Base64.getDecoder().decode(parts[1]);
            byte[] expected = Base64.getDecoder().decode(parts[2]);

            if (salt.length == 0 || expected.length == 0) {
                return false;
            }

            char[] chars = password.toCharArray();
            PBEKeySpec spec = new PBEKeySpec(
                chars, salt, iterations, expected.length * 8
            );

            try {
                SecretKeyFactory factory = SecretKeyFactory.getInstance(
                    "PBKDF2WithHmacSHA256"
                );
                byte[] actual = factory.generateSecret(spec).getEncoded();

                return MessageDigest.isEqual(actual, expected);
            } finally {
                spec.clearPassword();
                java.util.Arrays.fill(chars, '\0');
            }
        } catch (IllegalArgumentException |
                 NoSuchAlgorithmException |
                 InvalidKeySpecException e) {
            return false;
        }
    }

    public static boolean create_account(
        Map<String, String> store,
        String username,
        String password
    ) {
        if (store.containsKey(username)) {
            return false;
        }

        String record = hashPassword(password);
        store.put(username, record);
        return true;
    }

    public static boolean reset_password(
        Map<String, String> store,
        String username,
        String new_password,
        boolean authorized
    ) {
        if (!authorized || !store.containsKey(username)) {
            return false;
        }

        String record = hashPassword(new_password);
        store.put(username, record);
        return true;
    }

    public static boolean login(
        Map<String, String> store,
        String username,
        String password
    ) {
        if (!store.containsKey(username)) {
            return false;
        }

        return verifyPassword(password, store.get(username));
    }
}

```