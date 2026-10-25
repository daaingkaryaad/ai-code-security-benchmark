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