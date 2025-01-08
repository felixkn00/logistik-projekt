-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Erstellungszeit: 25. Nov 2024 um 08:42
-- Server-Version: 10.4.28-MariaDB
-- PHP-Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `logi_connect`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `deliveries`
--

CREATE TABLE `deliveries` (
  `DeliveryID` int(11) NOT NULL,
  `DeliveryNumber` text DEFAULT NULL,
  `SupplierName` text DEFAULT NULL,
  `Information` text DEFAULT NULL,
  `Price` float DEFAULT NULL,
  `DeliveryStatus` varchar(255) DEFAULT NULL,
  `DeliveryDate` date DEFAULT NULL,
  `UserID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `deliveries`
--

INSERT INTO `deliveries` (`DeliveryID`, `DeliveryNumber`, `SupplierName`, `Information`, `Price`, `DeliveryStatus`, `DeliveryDate`, `UserID`) VALUES
(26, 'sd', 'sdf', '2w', 2342, '234', '2024-11-23', 1),
(30, 'ewr', 'ew', 'rew', 2, '2', '2024-11-23', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `delivery_details`
--

CREATE TABLE `delivery_details` (
  `DeliveryItemID` int(11) NOT NULL,
  `DeliveryID` int(11) NOT NULL,
  `Article` text DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `SinglePrice` float DEFAULT NULL,
  `GraduatedPrice` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `delivery_details`
--

INSERT INTO `delivery_details` (`DeliveryItemID`, `DeliveryID`, `Article`, `Quantity`, `SinglePrice`, `GraduatedPrice`, `UserID`) VALUES
(5, 26, '234', 234, 2343, 324, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `inventory`
--

CREATE TABLE `inventory` (
  `ItemID` int(11) NOT NULL,
  `ItemNumber` varchar(50) NOT NULL,
  `ItemName` varchar(255) DEFAULT NULL,
  `Category` varchar(255) DEFAULT NULL,
  `StockQuantity` text DEFAULT NULL,
  `SinglePrice` float DEFAULT NULL,
  `GraduatedPrice` float DEFAULT NULL,
  `ExpiryDate` date DEFAULT NULL,
  `UserID` int(11) DEFAULT NULL,
  `moved` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `inventory`
--

INSERT INTO `inventory` (`ItemID`, `ItemNumber`, `ItemName`, `Category`, `StockQuantity`, `SinglePrice`, `GraduatedPrice`, `ExpiryDate`, `UserID`, `moved`) VALUES
(37, '43', 'dsffd', '', '', 234, 333, '2024-11-23', 1, 0),
(38, 'asdsad', 'sdaads', '', '', 222, 12312, '2024-11-23', 1, 0),
(39, 'sdf', 'sdaf', '', '', 123, 213, '2024-11-24', 1, 0),
(40, 'Felix', 'sdamkdsalmkld', NULL, NULL, 231, 1232, '2024-11-24', 1, 0),
(41, 'Fewlri', 'ewre', '', '', 2342, 234, '2024-11-24', 1, 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `scarce_commodity`
--

CREATE TABLE `scarce_commodity` (
  `StorageID` int(11) NOT NULL,
  `ItemID` int(11) DEFAULT NULL,
  `Donated` int(11) DEFAULT NULL,
  `ThrownAway` int(11) DEFAULT NULL,
  `Returned` int(11) DEFAULT NULL,
  `Repaired` int(11) DEFAULT NULL,
  `SinglePrice` float DEFAULT NULL,
  `GraduatedPrice` float DEFAULT NULL,
  `UserID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `scarce_commodity`
--

INSERT INTO `scarce_commodity` (`StorageID`, `ItemID`, `Donated`, `ThrownAway`, `Returned`, `Repaired`, `SinglePrice`, `GraduatedPrice`, `UserID`) VALUES
(8, 40, NULL, NULL, NULL, NULL, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user_account`
--

CREATE TABLE `user_account` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `access_token` text DEFAULT NULL,
  `refresh_token` text DEFAULT NULL,
  `can_create` tinyint(1) NOT NULL DEFAULT 0,
  `can_read` tinyint(1) NOT NULL DEFAULT 0,
  `can_update` tinyint(1) NOT NULL DEFAULT 0,
  `can_delete` tinyint(1) NOT NULL DEFAULT 0,
  `isSuperuser` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `user_account`
--

INSERT INTO `user_account` (`UserID`, `Username`, `Password`, `Email`, `access_token`, `refresh_token`, `can_create`, `can_read`, `can_update`, `can_delete`, `isSuperuser`) VALUES
(1, 'Felix', 'kreuz2', 'felix@email.com', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.JFF6rHhsW5I0kV2Src-sLDi1EuwX62NvRVKFbSmMDsg', 'fa88904c653059bc025f5231512f457be6611b741b02127403e23c9f0decc8ad8888a3e1f47290b10bb4855249d88db9cebc4547305f79b050e613e7983c21b6', 1, 1, 1, 1, 1);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `deliveries`
--
ALTER TABLE `deliveries`
  ADD PRIMARY KEY (`DeliveryID`),
  ADD KEY `fk_userid_useraccount` (`UserID`);

--
-- Indizes für die Tabelle `delivery_details`
--
ALTER TABLE `delivery_details`
  ADD PRIMARY KEY (`DeliveryItemID`),
  ADD KEY `DeliveryID` (`DeliveryID`),
  ADD KEY `fk_userid_useraccount` (`UserID`);

--
-- Indizes für die Tabelle `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`ItemID`);

--
-- Indizes für die Tabelle `scarce_commodity`
--
ALTER TABLE `scarce_commodity`
  ADD PRIMARY KEY (`StorageID`),
  ADD KEY `ItemID` (`ItemID`),
  ADD KEY `fk_uid` (`UserID`);

--
-- Indizes für die Tabelle `user_account`
--
ALTER TABLE `user_account`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `deliveries`
--
ALTER TABLE `deliveries`
  MODIFY `DeliveryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT für Tabelle `delivery_details`
--
ALTER TABLE `delivery_details`
  MODIFY `DeliveryItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT für Tabelle `inventory`
--
ALTER TABLE `inventory`
  MODIFY `ItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT für Tabelle `scarce_commodity`
--
ALTER TABLE `scarce_commodity`
  MODIFY `StorageID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT für Tabelle `user_account`
--
ALTER TABLE `user_account`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `delivery_details`
--
ALTER TABLE `delivery_details`
  ADD CONSTRAINT `delivery_details_ibfk_1` FOREIGN KEY (`DeliveryID`) REFERENCES `deliveries` (`DeliveryID`),
  ADD CONSTRAINT `fk_userid_useraccount` FOREIGN KEY (`UserID`) REFERENCES `user_account` (`UserID`);

--
-- Constraints der Tabelle `scarce_commodity`
--
ALTER TABLE `scarce_commodity`
  ADD CONSTRAINT `fk_uid` FOREIGN KEY (`UserID`) REFERENCES `user_account` (`UserID`),
  ADD CONSTRAINT `scarce_commodity_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `inventory` (`ItemID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
