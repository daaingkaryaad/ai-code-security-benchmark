download solution.java

```
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class Solution {
    public static int profile_update(Connection connection, String username, String new_email)
            throws SQLException {
        String sql = "UPDATE profiles SET email = ? WHERE username = ? COLLATE BINARY";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, new_email);
            statement.setString(2, username);
            return statement.executeUpdate();
        }
    }
}
```

the solution uses parameterized sql, matches usernames exactly, and returns `0` or `1`. it closes only the prepared statement, leaving the supplied connection and transaction management untouched.

compiled successfully with java 17.