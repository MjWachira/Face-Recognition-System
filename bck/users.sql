-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 26, 2022 at 01:23 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flaskdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'Cairocoders', 'cairocoders@gmail.com', '$2b$12$7RXKIh40P94SdbmrKZH2V.UjbZoAMJ7tVfOQ4zc1nkGGC8ypaSyma'),
(0, 'John Mwangi Wachira', 'mjwachira1@gmail.com', '$2b$12$kkXSsKQjyaJh9eENL820aesshg2Lh.QqN89df3ibL/o10VJ/3OgAG'),
(0, 'Sally', 'sallym@gmail.com', '$2b$12$NPKl88ReG5IiGATSAZIOiet4VS3lzqFrrq8TwGtjfQc.Zbaxw/wve'),
(0, 'Steve Mwangi', 'stevemwas@gmail.com', '$2b$12$JVSMhXDtjDeK.pAc7q78Lehtk0QxTY4acrZB5u732y5av1GtIYkQi');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
