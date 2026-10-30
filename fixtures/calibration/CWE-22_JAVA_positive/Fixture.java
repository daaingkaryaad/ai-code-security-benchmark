import java.nio.file.*;
import java.io.IOException;
public class Fixture {
  public static String read_file(String root, String user_path) throws IOException {
    return Files.readString(Path.of(root).resolve(user_path));
  }
}
