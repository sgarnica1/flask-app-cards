-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-01-2022 a las 22:38:53
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
-- Estructura de tabla para la tabla `service_cards`
--

CREATE TABLE `service_cards` (
  `card_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `card_number` varchar(255) NOT NULL,
  `expiration_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `cvv` varchar(3) NOT NULL,
  `type` varchar(255) NOT NULL DEFAULT 'services',
  `loan` float NOT NULL,
  `payment` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `service_cards`
--

INSERT INTO `service_cards` (`card_id`, `user_id`, `card_number`, `expiration_date`, `cvv`, `type`, `loan`, `payment`) VALUES
(5, 6, '4815313635046002', '2023-01-06 04:26:38', '874', 'service', 5000, 0),
(6, 2, '4815313668457530', '2027-01-06 23:00:27', '503', 'service', 500000, 0),
(10, 5, '4815313605107457', '2027-01-10 18:58:36', '163', 'service', 18000, 0),
(11, 5, '4815313688397568', '2027-01-10 18:59:45', '466', 'service', 15606, 0),
(12, 3, '4815313683653015', '2027-01-11 01:28:31', '112', 'service', 18000, 0),
(13, 13, '4815313696396297', '2027-01-11 01:47:10', '324', 'service', 0, 0),
(14, 1, '4815313692747533', '2027-01-11 01:55:32', '281', 'service', 18000, 0),
(15, 6, '4815313673317559', '2027-01-11 17:05:10', '369', 'service', 856030, 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `service_cards`
--
ALTER TABLE `service_cards`
  ADD PRIMARY KEY (`card_id`),
  ADD UNIQUE KEY `card_number` (`card_number`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `service_cards`
--
ALTER TABLE `service_cards`
  MODIFY `card_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `service_cards`
--
ALTER TABLE `service_cards`
  ADD CONSTRAINT `service_cards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
