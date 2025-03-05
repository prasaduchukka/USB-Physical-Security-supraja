<?php
// Getting data from the form (signup.php)
$firstname = $_POST['firstname'];
$lastname = $_POST['lastname'];
$gender = $_POST['gender'];
$email = $_POST['email'];
$password = $_POST['password'];

// Hashing the password before storing it in the database
$hashed_password = password_hash($password, PASSWORD_DEFAULT);  // Hashing password for security

// Database connection
$conn = new mysqli('localhost', 'root', '', 'test');

// Check if the connection was successful
if ($conn->connect_error) {
    echo "$conn->connect_error";
    die("Connection Failed: " . $conn->connect_error);
} else {
    // Preparing the SQL query to insert user data into the registration table
    $stmt = $conn->prepare("INSERT INTO registration (firstname, lastname, gender, email, password) VALUES (?, ?, ?, ?, ?)");
    
    // Binding parameters to the SQL;
    
    // Checking if the registration was successful
    if ($execval) {
        echo "Registration successful...";
    } else {
        echo "Error in registrati query
    $stmt->bind_param("sssss", $firstname, $lastname, $gender, $email, $hashed_password);
    
    // Executing the query
    $execval = $stmt->execute()on.";
    }

    // Closing the prepared statement and database connection
    $stmt->close();
    $conn->close();
}
?>
