```
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {

    public static long file_size(String root, String relative_path) throws IOException {
        Path rootPath = Paths.get(root).toAbsolutePath().normalize();
        Path relativePath = Paths.get(relative_path);

        if (relativePath.isAbsolute()) {
            throw new IllegalArgumentException("absolute paths are not allowed");
        }

        Path targetPath = rootPath.resolve(relativePath).normalize();

        if (!targetPath.startsWith(rootPath)) {
            throw new SecurityException("path escapes the root directory");
        }

        if (!Files.isRegularFile(targetPath)) {
            throw new IOException("file does not exist or is not a regular file");
        }

        return Files.size(targetPath);
    }
}
```

filename: `Solution.java`

the method resolves the supplied path relative to the root, prevents directory traversal outside the root, rejects absolute paths and directory targets, and returns the file size in bytes without modifying the filesystem.

time complexity: o(n), where n is the path length, plus filesystem operations.

space complexity: o(n) for path processing.