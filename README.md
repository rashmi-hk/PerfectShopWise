# E-commerce Website README

## Overview

Welcome to our E-commerce website! This document provides an overview of the website's features and functionalities for both administrators and users. The website allows users to window shop without login, but for shopping and other actions, user registration is required. The website also offers password reset and profile editing functionality.

## Entry Points

### 1. Admin Login
URL: [http://127.0.0.1:8000/admin_utility_login](http://127.0.0.1:8000/admin_utility_login)

This is the login page for administrators. Here, administrators can log in using their credentials to access the administrative features of the website. Once logged in, admins can add inventory, manage product quantity, add images, and categorize products.

### 2. User Login
URL: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)

This is the login page for users. Users can register and log in using their email and password. If a user is already registered, they can log in and continue shopping. However, if they are new users, they need to register and verify their account using OTP received via email.

### 3. Admin Dashboard
URL: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

The admin dashboard provides administrators with a comprehensive view of the website's activities. From here, admins can view order details, summaries, and update the order status. They can also access the Django admin interface for inventory management and other administrative tasks.

## Features

### 1. User Window Shopping
Users can browse the website without logging in. They can explore product categories, view product images, and read descriptions.

### 2. User Registration and OTP Verification
To place orders or add items to the cart, users need to register. Upon registration, users will receive an OTP via email. They can verify their account using this OTP.

### 3. User Cart and Placing Orders
After registration and login, users can add items to their cart. Once they have all desired items in the cart, they can proceed to checkout and place their order.

### 4. Forgot Password
Users who forget their passwords can use the "Forgot Password" functionality. They can enter their registered email address, and a password reset link will be sent to their email. Clicking the link will allow them to set a new password.

### 5. Profile Editing
Logged-in users can edit their profile information, such as name, address, and contact details. They can also change their password from the profile page.

### 6. Wishlist
Users can add products to their wishlist, making it easier to return to those items for future purchases.

### 7. Admin Inventory Management
Administrators have access to the admin dashboard, where they can manage inventory, update product quantity, add images, and categorize products.

### 8. Admin Order Management
Admins can view order details and summaries, and they have the ability to update the order status based on the progress of each order.

## Conclusion

Our E-commerce website aims to provide users with a seamless shopping experience while offering robust administrative capabilities for inventory and order management. We hope you enjoy using our platform, and please feel free to contact us if you have any questions or feedback. Happy shopping!
