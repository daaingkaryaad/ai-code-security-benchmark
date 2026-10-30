import java.sql.*;
public class Fixture {
  public static ResultSet lookup(Connection connection, String name) throws SQLException {
    String sql = "SELECT id FROM customers WHERE name = '" + name + "'";
    return connection.createStatement().executeQuery(sql);
  }
}
