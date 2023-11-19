CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `accounts` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    `first_name` varchar(50) NOT NULL,
    `last_name` varchar(50) NOT NULL,
    `dob` date NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `accounts` (`id`, `username`, `password`, `email`) 
VALUES (1,'test', 'test', 'test@test.com');

CREATE TABLE IF NOT EXISTS `machine_learning_models` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `model_name` varchar(255) NOT NULL,
    `description` text,
    `accuracy` float,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `machine_learning_models` (`model_name`, `description`, `accuracy`)
VALUES ('Random Forest', 'Modèle de classification basé sur Random Forest.', 0.92);