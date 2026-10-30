download solution.java

```
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Solution {
    public static List<String> directory_list(String root, String relative_path) throws IOException {
        Path rootPath = Paths.get(root);
        Path relativePath = Paths.get(relative_path);

        if (!rootPath.isAbsolute()) {
            throw new IllegalArgumentException("root must be absolute");
        }
        if (relativePath.isAbsolute()) {
            throw new IllegalArgumentException("relative_path must be relative");
        }

        rootPath = rootPath.normalize();
        Path target = rootPath.resolve(relativePath).normalize();
        if (!target.startsWith(rootPath)) {
            throw new IllegalArgumentException("path escapes root");
        }

        List<String> names = new ArrayList<>();
        try (DirectoryStream<Path> entries = Files.newDirectoryStream(target)) {
            for (Path entry : entries) {
                names.add(entry.getFileName().toString());
            }
        }

        Collections.sort(names);
        return names;
    }
}
```

compiled successfully with `javac`. uses only jdk standard libraries, rejects paths escaping the root, and returns sorted immediate directory entries without modifying the filesystem.