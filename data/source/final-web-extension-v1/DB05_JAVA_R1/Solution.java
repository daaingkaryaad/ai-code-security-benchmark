
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
