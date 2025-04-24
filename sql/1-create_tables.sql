-- Set up database settings
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    password_salt VARCHAR(32) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Clubs table
CREATE TABLE IF NOT EXISTS clubs (
    club_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stadium_name VARCHAR(255),
    stadium_seats INTEGER,
    coach_name VARCHAR(255),
    url VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Games table
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    date DATETIME NOT NULL,
    home_club_id VARCHAR(50) NOT NULL,
    away_club_id VARCHAR(50) NOT NULL,
    home_club_goals INTEGER NOT NULL DEFAULT 0,
    away_club_goals INTEGER NOT NULL DEFAULT 0,
    stadium VARCHAR(100) NOT NULL,
    attendance INTEGER,
    referee VARCHAR(100) NOT NULL,

    FOREIGN KEY (home_club_id) REFERENCES clubs(club_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (away_club_id) REFERENCES clubs(club_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE password_resets (
    reset_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
