CREATE DATABASE master;
USE master;
CREATE USER 'dwhistle' IDENTIFIED BY 'dwhistle';
GRANT ALL ON *.* TO 'dwhistle';
FLUSH PRIVILEGES;
CREATE TABLE user (
    id INT AUTO_INCREMENT,
    login VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    password_salt VARCHAR(63) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE profile (
    id INT AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    gender BIT(1) NOT NULL,
    city VARCHAR(40) NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES user(id)

);

CREATE TABLE profile_interests(
    profile_id INT NOT NULL,
    name VARCHAR(40),
    FOREIGN KEY(profile_id) REFERENCES profile(id)
);

CREATE TABLE user_friend_invites(
    user_id INT NOT NULL,
    friend_user_id INT NOT NULL,
    is_approved BIT(1) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(friend_user_id) REFERENCES user(id),
    UNIQUE KEY(user_id, friend_user_id)
);

DELIMITER //

CREATE PROCEDURE `friend_add`(IN in_user_id INT, IN in_friend_user_id INT)
BEGIN
DECLARE has_friend_approved INT;
SET has_friend_approved = (EXISTS(
SELECT 1
FROM user_friend_invites
WHERE user_id=in_friend_user_id AND friend_user_id=in_user_id AND is_approved = 1));

REPLACE INTO user_friend_invites
SET user_id = in_user_id,
   friend_user_id = in_friend_user_id,
   is_approved = 1;

REPLACE INTO user_friend_invites
SET user_id = in_friend_user_id,
   friend_user_id = in_user_id,
   is_approved = has_friend_approved;
END//
DELIMITER ;

GRANT ALL ON *.* TO 'dwhistle';
FLUSH PRIVILEGES;