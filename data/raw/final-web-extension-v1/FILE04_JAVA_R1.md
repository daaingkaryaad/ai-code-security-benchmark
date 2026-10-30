download solution.java

```
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

public class Solution {
    public static void file_copy(String root, String source_path, String destination_path)
            throws IOException {
        Path base = Paths.get(root).toAbsolutePath().normalize();
        Path source = resolveWithinRoot(base, source_path);
        Path destination = resolveWithinRoot(base, destination_path);

        if (!Files.isRegularFile(source)) {
            throw new IOException("Source must be an ordinary file: " + source);
        }
        if (!Files.isDirectory(destination.getParent())) {
            throw new IOException("Destination parent directory does not exist: " + destination.getParent());
        }

        Files.copy(source, destination, StandardCopyOption.REPLACE_EXISTING);
    }

    private static Path resolveWithinRoot(Path base, String relativePath) {
        Path candidate = Paths.get(relativePath);
        if (candidate.isAbsolute()) {
            throw new IllegalArgumentException("Absolute paths are not allowed: " + relativePath);
        }
        Path resolved = base.resolve(candidate).normalize();
        if (!resolved.startsWith(base)) {
            throw new IllegalArgumentException("Path escapes root: " + relativePath);
        }
        return resolved;
    }
}
```

the implementation uses only jdk standard libraries, validates both paths against the root, copies all bytes, replaces existing destination files, and preserves the source.

compilation verified with `javac`.