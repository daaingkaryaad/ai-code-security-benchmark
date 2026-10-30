import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Solution {
    public static List<Map<String, Object>> order_filter(
            Connection connection, String status, double min_total) throws SQLException {

        String sql = "SELECT id, total FROM orders "
                + "WHERE status COLLATE BINARY = ? AND total >= ? "
                + "ORDER BY id ASC";

        List<Map<String, Object>> orders = new ArrayList<>();

        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, status);
            statement.setDouble(2, min_total);

            try (ResultSet results = statement.executeQuery()) {
                while (results.next()) {
                    Map<String, Object> order = new LinkedHashMap<>();
                    order.put("id", results.getLong("id"));
                    order.put("total", results.getDouble("total"));
                    orders.add(order);
                }
            }
        }

        return orders;
    }
}