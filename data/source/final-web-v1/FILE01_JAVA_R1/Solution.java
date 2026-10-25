
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class Solution {

    public static String file_read(String root, String relative_path)
            throws IOException {

        Path rootPath = Path.of(root).toAbsolutePath().normalize();
        Path inputPath = Path.of(relative_path);

        if (inputPath.isAbsolute()) {
            throw new IllegalArgumentException("absolute paths are not allowed");
        }

        Path targetPath = rootPath.resolve(inputPath).normalize();

        if (!targetPath.startsWith(rootPath)) {
            throw new IllegalArgumentException("path is outside root");
        }

        return Files.readString(targetPath, StandardCharsets.UTF_8);
    }
}
