download solution.java

```

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class Solution {
    public static int cart_item_delete(Connection connection, String cart_id, String sku)
            throws SQLException {
        String sql = "DELETE FROM cart_items WHERE cart_id = ? AND sku = ?";

        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, cart_id);
            statement.setString(2, sku);
            return statement.executeUpdate();
        }
    }
}

```

the implementation uses a parameterized sql statement to match both `cart_id` and `sku` exactly.

- returns `1` when a row is deleted, or `0` when no matching row exists.
- leaves other cart items unchanged.
- closes the prepared statement without closing the supplied connection.
- does not commit, roll back, or modify the database schema.
- uses only java 17 standard libraries.