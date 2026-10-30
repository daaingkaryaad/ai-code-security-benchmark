```
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Solution {

    public static boolean file_delete(String root, String relative_path) throws IOException {
        Path rootPath = Path.of(root).toAbsolutePath().normalize();
        Path relativePath = Path.of(relative_path);

        if (relativePath.isAbsolute()) {
            throw new IllegalArgumentException("absolute paths are not allowed");
        }

        Path target = rootPath.resolve(relativePath).normalize();

        if (!target.startsWith(rootPath)) {
            throw new IllegalArgumentException("path escapes root directory");
        }

        if (!Files.exists(target)) {
            return false;
        }

        if (!Files.isRegularFile(target)) {
            throw new IOException("target is not an ordinary file");
        }

        return Files.deleteIfExists(target);
    }
}
```