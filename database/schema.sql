-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.3.10-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE TABLE IF NOT EXISTS `species` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `taxonomic_next` INT(11) DEFAULT NULL,
  `reference_image_fk` int(11) DEFAULT NULL,
  `common_name` tinytext NOT NULL,
  `binomial_name` tinytext NOT NULL,
  PRIMARY KEY (`pk`),
  UNIQUE INDEX `species_taxonomic_next` (`taxonomic_next`),
  KEY `species_reference_image` (`reference_image_fk`),
  CONSTRAINT `taxonomic_next` FOREIGN KEY (`taxonomic_next`) REFERENCES `species` (`pk`),
  CONSTRAINT `species_reference_image` FOREIGN KEY (`reference_image_fk`) REFERENCES `bird_image` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `site` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `reference_image_fk` int(11) DEFAULT NULL,
  `name` tinytext DEFAULT NULL,
  `lat_lon` point DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `site_reference_image` (`reference_image_fk`),
  CONSTRAINT `site_reference_image` FOREIGN KEY (`reference_image_fk`) REFERENCES `site_image` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `visit` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `site_fk` int(11) DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `visit_site` (`site_fk`),
  CONSTRAINT `visit_site` FOREIGN KEY (`site_fk`) REFERENCES `site` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `sighting` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `species_fk` int(11) NOT NULL,
  `visit_fk` int(11) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `uncertainty` int(11) DEFAULT NULL,
  `seen` BIT(1) NULL DEFAULT b'0',
  `heard` BIT(1) NULL DEFAULT b'0',
  `feral` BIT(1) NULL DEFAULT b'0',
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `sighting_species` (`species_fk`),
  KEY `sighting_visit` (`visit_fk`),
  CONSTRAINT `sighting_species` FOREIGN KEY (`species_fk`) REFERENCES `species` (`pk`),
  CONSTRAINT `sighting_visit` FOREIGN KEY (`visit_fk`) REFERENCES `visit` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `bird_image` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `sighting_fk` int(11) DEFAULT NULL,
  `path` tinytext NOT NULL,
  PRIMARY KEY (`pk`),
  KEY `bird_image_sighting` (`sighting_fk`),
  CONSTRAINT `bird_image_sighting` FOREIGN KEY (`sighting_fk`) REFERENCES `sighting` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `site_image` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `site_fk` int(11) DEFAULT 0,
  `path` tinytext NOT NULL DEFAULT '0',
  PRIMARY KEY (`pk`),
  KEY `site_image_site` (`site_fk`),
  CONSTRAINT `site_image_site` FOREIGN KEY (`site_fk`) REFERENCES `site` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE PROCEDURE get_list(
  IN time_start DATE,
  IN time_end DATE,
  IN site_pk INT,
  IN include_feral BIT
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
BEGIN

SELECT 
    common_name,
    binomial_name,
    SUM(count) as count,
    COUNT(sighting.pk) as times_seen,
    MAX(seen) as seen,
    MAX(heard) as heard
  FROM `species`
  JOIN `sighting` ON sighting.species_fk = species.pk
  JOIN `visit` ON sighting.visit_fk = visit.pk
  JOIN `site` ON visit.site_fk = site.pk
  WHERE ((time_start IS NULL OR start_time >= time_start) AND
         (time_end IS NULL OR end_time <= time_end)) AND
        (feral IS NULL OR feral != 1 OR feral = include_feral) AND
        (site_pk IS NULL OR site.pk = site_pk)
  GROUP BY species.pk;

END;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
