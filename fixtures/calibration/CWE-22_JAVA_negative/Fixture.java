import java.nio.file.*;
import java.io.IOException;
public class Fixture {
  public static String read_file(String root, String user_path) throws IOException {
    Path base = Path.of(root).toAbsolutePath().normalize();
    Path rel = Path.of(user_path);
    if (rel.isAbsolute()) throw new IllegalArgumentException("absolute path");
    Path target = base.resolve(rel).normalize();
    if (!target.startsWith(base)) throw new IllegalArgumentException("outside root");
    return Files.readString(target);
  }
}
