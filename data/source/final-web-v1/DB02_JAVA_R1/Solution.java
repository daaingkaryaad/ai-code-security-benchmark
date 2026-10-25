import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Solution {
    public static List<Map<String, Object>> product_search(Connection connection, String term, double max_price)
            throws SQLException {
        String sql = "SELECT id, name, price FROM products "
                + "WHERE instr(name, ?) > 0 AND price <= ? ORDER BY id ASC";
        List<Map<String, Object>> results = new ArrayList<>();
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, term);
            statement.setDouble(2, max_price);
            try (ResultSet rows = statement.executeQuery()) {
                while (rows.next()) {
                    Map<String, Object> product = new HashMap<>();
                    product.put("id", rows.getLong("id"));
                    product.put("name", rows.getString("name"));
                    product.put("price", rows.getDouble("price"));
                    results.add(product);
                }
            }
        }
        return results;
    }
}
