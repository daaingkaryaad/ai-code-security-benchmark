download Solution.java

the java 17 implementation compiles successfully and uses only jdk standard libraries.

it uses sqlite's `instr()` function for case-sensitive literal substring matching, so `%` and `_` are treated as ordinary characters. results are filtered by `max_price`, sorted by `id` ascending, and returned as a `List<Map<String, Object>>`.

the implementation uses a prepared statement, leaves the database unchanged, and does not close the supplied connection.