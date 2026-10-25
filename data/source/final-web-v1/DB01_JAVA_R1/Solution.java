
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Solution {

    public static List<Map<String, Object>> customer_lookup(
            Connection connection, String customer_name
    ) throws SQLException {

        String sql = "SELECT id, email FROM customers "
                   + "WHERE name = ? COLLATE BINARY "
                   + "ORDER BY id ASC";

        List<Map<String, Object>> results = new ArrayList<>();

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, customer_name);

            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    Map<String, Object> customer = new HashMap<>();

                    customer.put("id", rs.getLong("id"));
                    customer.put("email", rs.getString("email"));

                    results.add(customer);
                }
            }
        }

        return results;
    }
}
