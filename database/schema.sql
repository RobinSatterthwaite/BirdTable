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
  `taxonomic_first` BIT(1) DEFAULT NULL,
  `taxonomic_next` INT(11) DEFAULT NULL,
  `reference_image_fk` int(11) DEFAULT NULL,
  `common_name` tinytext NOT NULL,
  `binomial_name` tinytext NOT NULL,
  PRIMARY KEY (`pk`),
  UNIQUE INDEX `species_taxonomic_first` (`taxonomic_first`),
  UNIQUE INDEX `species_taxonomic_next` (`taxonomic_next`),
  KEY `species_reference_image` (`reference_image_fk`),
  CONSTRAINT `taxonomic_next` FOREIGN KEY (`taxonomic_next`) REFERENCES `species` (`pk`),
  CONSTRAINT `species_reference_image` FOREIGN KEY (`reference_image_fk`) REFERENCES `bird_image` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `geographic_area` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `parent_fk` int(11) DEFAULT NULL,
  `name` tinytext NOT NULL,
  PRIMARY KEY (`pk`),
  KEY `area_parent` (`parent_fk`),
  CONSTRAINT `area_parent` FOREIGN KEY (`parent_fk`) REFERENCES `geographic_area` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `site` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `area_fk` int(11) NOT NULL,
  `reference_image_fk` int(11) DEFAULT NULL,
  `name` tinytext DEFAULT NULL,
  `lat_lon` point DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `site_reference_image` (`reference_image_fk`),
  KEY `site_area` (`area_fk`),
  CONSTRAINT `site_area` FOREIGN KEY (`area_fk`) REFERENCES `geographic_area` (`pk`),
  CONSTRAINT `site_reference_image` FOREIGN KEY (`reference_image_fk`) REFERENCES `site_image` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `visit` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `site_fk` int(11) DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `notes` text DEFAULT NULL,
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
  `seen` BIT(1) DEFAULT b'0',
  `heard` BIT(1) DEFAULT b'0',
  `feral` BIT(1) DEFAULT b'0',
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `sighting_species` (`species_fk`),
  KEY `sighting_visit` (`visit_fk`),
  CONSTRAINT `sighting_species` FOREIGN KEY (`species_fk`) REFERENCES `species` (`pk`),
  CONSTRAINT `sighting_visit` FOREIGN KEY (`visit_fk`) REFERENCES `visit` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `incidental_sighting` (
  `pk` INT(11) NOT NULL AUTO_INCREMENT,
  `species_fk` INT(11) NOT NULL,
  `site_fk` INT(11) NOT NULL,
  `time` DATETIME NOT NULL,
  `count` INT(11) DEFAULT NULL,
  `uncertainty` INT(11) DEFAULT NULL,
  `seen` BIT(1) NULL DEFAULT b'0',
  `heard` BIT(1) NULL DEFAULT b'0',
  `feral` BIT(1) NULL DEFAULT b'0',
  `notes` TEXT DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `incidental_sighting_species` (`species_fk`),
  KEY `incidental_sighting_site` (`site_fk`),
  CONSTRAINT `incidental_sighting_species` FOREIGN KEY (`species_fk`) REFERENCES `species` (`pk`),
  CONSTRAINT `incidental_sighting_site` FOREIGN KEY (`site_fk`) REFERENCES `site` (`pk`)
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
  IN start_date DATETIME,
  IN end_date DATETIME,
  IN site_pks VARCHAR(16384),
  IN include_feral BIT
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
BEGIN

SELECT
    pk, 
    common_name,
    binomial_name,
    CAST(SUM(count) AS INT) AS count,
    COUNT(*) AS times_seen,
    CAST(MAX(seen) AS INT) AS seen,
    CAST(MAX(heard) AS INT) AS heard
FROM (
  SELECT
      species.pk as pk,
      common_name,
      binomial_name,
      count,
      sighting.pk as s_pk,
      seen,
      heard
  FROM `species`
  JOIN `sighting` ON sighting.species_fk = species.pk
  JOIN `visit` ON sighting.visit_fk = visit.pk
  WHERE ((start_date IS NULL OR start_time >= start_date) AND
         (end_date IS NULL OR end_time <= end_date)) AND
        (feral IS NULL OR feral != 1 OR feral = include_feral) AND
        (site_pks IS NULL OR FIND_IN_SET(visit.site_fk, site_pks))
  UNION
  SELECT
      species.pk as pk,
      common_name,
      binomial_name,
      count,
      incidental_sighting.pk as is_pk,
      seen,
      heard
      FROM `species`
      JOIN `incidental_sighting` ON incidental_sighting.species_fk = species.pk
    WHERE ((start_date IS NULL OR incidental_sighting.time >= start_date) AND
           (end_date IS NULL OR incidental_sighting.time <= end_date)) AND
          (feral IS NULL OR feral != 1 OR feral = include_feral) AND
          (site_pks IS NULL OR FIND_IN_SET(site_fk, site_pks))
  ) as t_1
GROUP BY pk;

END;

CREATE PROCEDURE get_site_info()
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
BEGIN

SELECT pk, parent_fk, name
  FROM geographic_area
  ORDER BY parent_fk;

SELECT pk, area_fk, name, lat_lon
  FROM site;

END;


CREATE PROCEDURE get_taxonomic_order()
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
BEGIN

WITH RECURSIVE taxonomic_order (pk, taxonomic_next, common_name) AS (
  SELECT pk, taxonomic_next, common_name
    FROM species
    WHERE taxonomic_first = 1
  UNION ALL
  SELECT s.pk, s.taxonomic_next, s.common_name
    FROM species s
    JOIN taxonomic_order ON taxonomic_order.taxonomic_next = s.pk
)
SELECT pk, common_name FROM taxonomic_order;

END;


CREATE PROCEDURE get_visit(
  IN visit_pk INT
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
BEGIN

SELECT
    site.name AS site_name,
    site.pk AS site_pk,
    visit.start_time,
    visit.end_time,
    visit.notes
  FROM `visit`
  JOIN `site` ON site.pk = visit.site_fk
  WHERE visit.pk = visit_pk;

SELECT
    species_fk AS species_pk,
    count,
    uncertainty,
    seen,
    heard,
    feral,
    notes
  FROM `sighting`
  WHERE sighting.visit_fk = visit_pk;

END;


CREATE PROCEDURE get_visits(
  IN start_date DATETIME,
  IN end_date DATETIME,
  IN site_pk INT,
  IN species_pk INT,
  IN limit_size INT,
  IN start_index INT
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
BEGIN

CREATE TEMPORARY TABLE `searched_visits` (
  pk int,
  site_name tinytext,
  start_time datetime,
  end_time datetime);

CREATE TEMPORARY TABLE `selected_visits` (
  pk int,
  site_name tinytext,
  start_time datetime,
  end_time datetime);

INSERT INTO `searched_visits`
  SELECT
    visit.pk as pk,
    name as site_name,
    start_time,
    end_time
  FROM `visit`
  JOIN `site` ON site.pk = visit.site_fk
  JOIN `sighting` ON visit.pk = sighting.visit_fk
  WHERE ((start_date IS NULL OR start_time >= start_date) AND
         (end_date IS NULL OR end_time <= end_date)) AND
        (site_pk IS NULL OR visit.site_fk = site_pk) AND
        (species_pk IS NULL OR sighting.species_fk = species_pk)
  GROUP BY visit.pk
  ORDER BY start_time DESC;

INSERT INTO `selected_visits`
  SELECT *
  FROM `searched_visits`
  LIMIT limit_size
  OFFSET start_index;

SELECT * FROM `selected_visits`;

SELECT
    visit_fk as visit_pk,
    species_fk as species_pk,
    count,
    seen,
    heard,
    feral
  FROM `sighting`
  INNER JOIN `selected_visits` ON visit_fk = selected_visits.pk
  ORDER BY visit_pk;

SELECT COUNT(*) FROM `searched_visits`;

DROP TABLE `searched_visits`;
DROP TABLE `selected_visits`;

END;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
