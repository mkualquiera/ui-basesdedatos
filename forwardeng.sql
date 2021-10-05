-- MySQL Script generated by MySQL Workbench
-- Mon 04 Oct 2021 06:49:25 PM -05
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema promoterdb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `promoterdb` ;

-- -----------------------------------------------------
-- Schema promoterdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `promoterdb` ;
USE `promoterdb` ;

-- -----------------------------------------------------
-- Table `promoterdb`.`chain`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`chain` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`chain` (
  `chainid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `chainname` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`chainid`),
  UNIQUE INDEX `idchain_UNIQUE` (`chainid` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`city`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`city` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`city` (
  `cityid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cityname` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`cityid`),
  UNIQUE INDEX `idchain_UNIQUE` (`cityid` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`pos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`pos` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`pos` (
  `posid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `poschainid` INT UNSIGNED NOT NULL,
  `poscityid` INT UNSIGNED NOT NULL,
  `posaddress` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`posid`),
  UNIQUE INDEX `idpos_UNIQUE` (`posid` ASC) VISIBLE,
  INDEX `fk_pos_chain_idx` (`poschainid` ASC) VISIBLE,
  INDEX `fk_pos_city1_idx` (`poscityid` ASC) VISIBLE,
  CONSTRAINT `fk_pos_chain`
    FOREIGN KEY (`poschainid`)
    REFERENCES `promoterdb`.`chain` (`chainid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pos_city1`
    FOREIGN KEY (`poscityid`)
    REFERENCES `promoterdb`.`city` (`cityid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`personal_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`personal_info` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`personal_info` (
  `infoid` INT UNSIGNED NOT NULL,
  `infoname` VARCHAR(45) NOT NULL,
  `infophone` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`infoid`),
  UNIQUE INDEX `id_UNIQUE` (`infoid` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`promoter`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`promoter` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`promoter` (
  `promoterposid` INT UNSIGNED NOT NULL,
  `promoterinfoid` INT UNSIGNED NOT NULL,
  INDEX `fk_promoter_pos1_idx` (`promoterposid` ASC) VISIBLE,
  PRIMARY KEY (`promoterinfoid`),
  CONSTRAINT `fk_promoter_pos1`
    FOREIGN KEY (`promoterposid`)
    REFERENCES `promoterdb`.`pos` (`posid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_promoter_personal_info1`
    FOREIGN KEY (`promoterinfoid`)
    REFERENCES `promoterdb`.`personal_info` (`infoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`trainer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`trainer` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`trainer` (
  `trainerinfoid` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`trainerinfoid`),
  CONSTRAINT `fk_trainer_personal_info1`
    FOREIGN KEY (`trainerinfoid`)
    REFERENCES `promoterdb`.`personal_info` (`infoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`subject`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`subject` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`subject` (
  `subjectid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `subjectname` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`subjectid`),
  UNIQUE INDEX `idsubject_UNIQUE` (`subjectid` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`capacitation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`capacitation` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`capacitation` (
  `capacitationid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `capacitationpromoterinfoid` INT UNSIGNED NOT NULL,
  `capacitationtrainerinfoid` INT UNSIGNED NOT NULL,
  `capacitationdate` DATE NOT NULL,
  `capacitationsubjectid` INT UNSIGNED NOT NULL,
  `capacitationgrade` INT NOT NULL,
  PRIMARY KEY (`capacitationid`),
  UNIQUE INDEX `idcapacitation_UNIQUE` (`capacitationid` ASC) VISIBLE,
  INDEX `fk_capacitation_promoter1_idx` (`capacitationpromoterinfoid` ASC) VISIBLE,
  INDEX `fk_capacitation_trainer1_idx` (`capacitationtrainerinfoid` ASC) VISIBLE,
  INDEX `fk_capacitation_subject1_idx` (`capacitationsubjectid` ASC) VISIBLE,
  CONSTRAINT `fk_capacitation_promoter1`
    FOREIGN KEY (`capacitationpromoterinfoid`)
    REFERENCES `promoterdb`.`promoter` (`promoterinfoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_capacitation_trainer1`
    FOREIGN KEY (`capacitationtrainerinfoid`)
    REFERENCES `promoterdb`.`trainer` (`trainerinfoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_capacitation_subject1`
    FOREIGN KEY (`capacitationsubjectid`)
    REFERENCES `promoterdb`.`subject` (`subjectid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`supervisor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`supervisor` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`supervisor` (
  `supervisorinfoid` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`supervisorinfoid`),
  CONSTRAINT `fk_supervisor_personal_info1`
    FOREIGN KEY (`supervisorinfoid`)
    REFERENCES `promoterdb`.`personal_info` (`infoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`evaluation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`evaluation` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`evaluation` (
  `evaluationid` INT NOT NULL,
  `evaluationsupervisorinfoid` INT UNSIGNED NOT NULL,
  `evaluationpromoterinfoid` INT UNSIGNED NOT NULL,
  `evaluationdate` DATE NOT NULL,
  `evaluationcomments` TEXT NULL,
  PRIMARY KEY (`evaluationid`),
  INDEX `fk_evaluation_supervisor1_idx` (`evaluationsupervisorinfoid` ASC) VISIBLE,
  INDEX `fk_evaluation_promoter1_idx` (`evaluationpromoterinfoid` ASC) VISIBLE,
  CONSTRAINT `fk_evaluation_supervisor1`
    FOREIGN KEY (`evaluationsupervisorinfoid`)
    REFERENCES `promoterdb`.`supervisor` (`supervisorinfoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluation_promoter1`
    FOREIGN KEY (`evaluationpromoterinfoid`)
    REFERENCES `promoterdb`.`promoter` (`promoterinfoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promoterdb`.`trainer_has_subject`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promoterdb`.`trainer_has_subject` ;

CREATE TABLE IF NOT EXISTS `promoterdb`.`trainer_has_subject` (
  `trainerinfoid` INT UNSIGNED NOT NULL,
  `subjectid` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`trainerinfoid`, `subjectid`),
  INDEX `fk_trainer_has_subject_subject1_idx` (`subjectid` ASC) VISIBLE,
  INDEX `fk_trainer_has_subject_trainer1_idx` (`trainerinfoid` ASC) VISIBLE,
  CONSTRAINT `fk_trainer_has_subject_trainer1`
    FOREIGN KEY (`trainerinfoid`)
    REFERENCES `promoterdb`.`trainer` (`trainerinfoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_trainer_has_subject_subject1`
    FOREIGN KEY (`subjectid`)
    REFERENCES `promoterdb`.`subject` (`subjectid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
