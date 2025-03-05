<?php
session_start();

// Database connection
$conn = new mysqli('localhost', 'root', '', 'test');

// Check connection
if ($conn->connect_error) {
    die("Connection Failed: " . $conn->connect_error);
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] == "POST") {
    // Trim and sanitize input
    $email = trim($_POST['email']);
    $password = trim($_POST['password']);

    // Validate input
    if (!empty($email) && !empty($password) && !is_numeric($email)) {
        // Prepare the SQL query
        $query = "SELECT * FROM registration WHERE email = ? LIMIT 1";
        $stmt = $conn->prepare($query);
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result && $result->num_rows > 0) {
            // Fetch user data
            $user_data = $result->fetch_assoc();

            // Verify password
            if (password_verify($password, $user_data['password'])) {
                // Store user session details
                $_SESSION['user_id'] = $user_data['id'];
                $_SESSION['user_email'] = $user_data['email'];

                // Command to run app.py in the background (Windows)
                $python_command = 'python C:/xampp/htdocs/form/app.py';
                //C:\form\app.py
                pclose(popen("start /B " . $python_command, "r")); // Runs Python script in the background

                // Redirect to a success page (or directly to index.php)
                header("Location: index.php");
                exit;
            } else {
                echo "<script>alert('Wrong password entered');</script>";
            }
        } else {
            echo "<script>alert('No user found with this email');</script>";
        }
    } else {
        echo "<script>alert('Please enter valid credentials');</script>";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="login">
        <h1>Login Page</h1>
        <form method="POST" action="login.php">
            <label>Email</label>
            <input type="email" name="email" required>

            <label>Password</label>
            <input type="password" name="password" required>

            <input type="submit" value="Login">
        </form>
        <p>Don't have an account? <a href="signup.php">Sign up here</a></p>
    </div>
</body>
</html>
