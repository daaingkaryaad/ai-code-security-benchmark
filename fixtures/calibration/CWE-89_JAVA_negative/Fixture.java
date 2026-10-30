import java.sql.*;
public class Fixture {
  public static ResultSet lookup(Connection connection, String name) throws SQLException {
    PreparedStatement stmt = connection.prepareStatement("SELECT id FROM customers WHERE name = ?");
    stmt.setString(1, name);
    return stmt.executeQuery();
  }
}
