download solution.java

the java 17 implementation compiles successfully and uses only jdk standard libraries.

it includes the required `public static void file_write(String root, String relative_path, String content)` method, validates that paths remain within the absolute root directory, rejects absolute and escaping paths, and writes utf-8 content while creating or overwriting the target file. parent directories must already exist.