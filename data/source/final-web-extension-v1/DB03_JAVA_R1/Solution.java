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