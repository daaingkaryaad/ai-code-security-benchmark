`Solution.java`

```

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class Solution {

    public static int ticket_count(Connection connection, String owner, String status)
            throws SQLException {

        String sql = "SELECT COUNT(*) FROM tickets WHERE owner = ? AND status = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, owner);
            stmt.setString(2, status);

            try (ResultSet rs = stmt.executeQuery()) {
                return rs.next() ? rs.getInt(1) : 0;
            }
        }
    }
}

```

the solution uses a parameterized query to match `owner` and `status`, preventing sql injection. `count(*)` returns `0` when no rows match.

the supplied connection remains open, and the database is unchanged. only the statement and result set are closed.

the code is compatible with java 17 and uses standard jdk libraries.