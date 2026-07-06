def generate_response(user_message):

    message = user_message.lower()

    if "python" in message:
        return """Python Example:

print("Hello, World!")
"""

    elif "php" in message:
        return """PHP Example:

<?php
echo "Hello, World!";
?>
"""

    elif "c++" in message or "cpp" in message:
        return """C++ Example:

#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!";
    return 0;
}
"""

    elif "c program" in message or message == "c":
        return """C Example:

#include <stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}
"""

    elif "java" in message:
        return """Java Example:

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""

    elif "html" in message:
        return """HTML Example:

<!DOCTYPE html>
<html>
<head>
<title>My Page</title>
</head>
<body>

<h1>Hello World</h1>

</body>
</html>
"""

    elif "css" in message:
        return """CSS Example:

body{
    background:white;
    color:black;
}
"""

    elif "javascript" in message or "js" in message:
        return """JavaScript Example:

console.log("Hello World");
"""

    elif "sql" in message:
        return """SQLite Example:

CREATE TABLE students(
    id INTEGER PRIMARY KEY,
    name TEXT
);
"""

    else:
        return (
            "I can help you generate code in:\n\n"
            "• Python\n"
            "• PHP\n"
            "• C\n"
            "• C++\n"
            "• Java\n"
            "• HTML\n"
            "• CSS\n"
            "• JavaScript\n"
            "• SQL\n\n"
            "Example:\n"
            "'Create a Python program to calculate factorial.'"
        )