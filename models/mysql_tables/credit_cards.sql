-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-01-2022 a las 22:38:07
-- Versión del servidor: 10.4.17-MariaDB
-- Versión de PHP: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `flask_app_cards`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `credit_cards`
--

CREATE TABLE `credit_cards` (
  `card_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `card_number` varchar(255) NOT NULL,
  `expiration_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `cvv` int(11) NOT NULL,
  `type` varchar(255) NOT NULL DEFAULT 'credit',
  `interest_rate` float NOT NULL,
  `loan` int(11) DEFAULT NULL,
  `payment` int(11) DEFAULT NULL,
  `new_charges` int(11) DEFAULT NULL,
  `new_loan` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `credit_cards`
--

INSERT INTO `credit_cards` (`card_id`, `user_id`, `card_number`, `expiration_date`, `cvv`, `type`, `interest_rate`, `loan`, `payment`, `new_charges`, `new_loan`) VALUES
(2, 3, '4152313447759022', '2027-01-04 19:08:52', 986, 'credit', 12, 0, 100, 0, 0),
(5, 1, '4152313442405630', '2027-01-04 19:08:55', 193, 'credit', 11, 266500, 6001, 0, 499290),
(6, 2, '4152313465968877', '2027-01-04 19:08:57', 302, 'credit', 16, 2500, 1000, 50, 0),
(8, 1, '4152313439457064', '2027-01-04 19:09:02', 991, 'credit', 12, 33900, 150, 0, 67500),
(10, 6, '4152313414060227', '2027-01-05 19:09:06', 352, 'credit', 16, 15000, 2000, 0, 30333),
(12, 5, '4152313416299215', '2027-01-06 03:58:32', 158, 'credit', 15, 0, 20, 0, 0),
(13, 6, '4152313419618016', '2027-01-06 04:26:50', 315, 'credit', 15, 3000, 30, 20, 6702),
(18, 13, '4152313411847390', '2027-01-10 17:48:57', 603, 'credit', 18, 1500, 1500, 50, 50),
(22, 13, '4152313441973137', '2027-01-11 16:21:30', 536, 'credit', 18, 3500, 1500, 6500, 11500),
(23, 5, '4152313437133393', '2027-01-11 16:28:11', 162, 'credit', 16, 0, 500000, 8000000, 8000000),
(24, 13, '4152313408452626', '2027-01-11 16:56:53', 960, 'credit', 15, 0, 300, 300, 300);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `credit_cards`
--
ALTER TABLE `credit_cards`
  ADD PRIMARY KEY (`card_id`),
  ADD UNIQUE KEY `card_number` (`card_number`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `credit_cards`
--
ALTER TABLE `credit_cards`
  MODIFY `card_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `credit_cards`
--
ALTER TABLE `credit_cards`
  ADD CONSTRAINT `credit_cards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
