<?php
session_start();  // Start the session

// Check if the user is logged in (by checking if the session variable is set)
if (!isset($_SESSION['user_id'])) {
    // If not logged in, redirect to the login page
    header("Location: login.php");
    die;
}

// Include db.php only if necessary, it's already included in other files
// include('db.php');  // If you need to fetch data from the database, you can include this file here
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <h1>Welcome, User!</h1>
    
    <!-- Logout link to destroy the session -->
    <a href="logout.php">Logout</a>  <!-- Added a logout page link -->
</body>
</html>
