import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class Solution {
    public static void file_write(String root, String relative_path, String content) throws IOException {
        Path rootPath = Paths.get(root);
        if (!rootPath.isAbsolute()) {
            throw new IllegalArgumentException("root must be an absolute path");
        }

        Path relativePath = Paths.get(relative_path);
        if (relativePath.isAbsolute()) {
            throw new IllegalArgumentException("path must be relative to root");
        }

        Path normalizedRoot = rootPath.normalize();
        Path target = normalizedRoot.resolve(relativePath).normalize();
        if (!target.startsWith(normalizedRoot)) {
            throw new IllegalArgumentException("path resolves outside root");
        }

        Files.writeString(target, content, StandardCharsets.UTF_8,
                StandardOpenOption.CREATE,
                StandardOpenOption.TRUNCATE_EXISTING,
                StandardOpenOption.WRITE);
    }
}
