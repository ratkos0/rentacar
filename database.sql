-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb3 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`rent_a_car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`rent_a_car` (
  `Naziv` VARCHAR(45) NOT NULL,
  `Adresa` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Broj_telefona` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Naziv`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`auta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`auta` (
  `Rent_a_car_Naziv` VARCHAR(45) NOT NULL,
  `Broj_sasije` CHAR(17) NOT NULL,
  `Marka` VARCHAR(45) NOT NULL,
  `Model` VARCHAR(45) NOT NULL,
  `Godina_proizvodnje` VARCHAR(45) NOT NULL,
  `Motor` FLOAT NOT NULL,
  `kW` INT NOT NULL,
  `hp` INT NOT NULL,
  `Cijena` FLOAT NOT NULL,
  PRIMARY KEY (`Rent_a_car_Naziv`, `Broj_sasije`),
  INDEX `fk_Auta_Rent_a_car1_idx` (`Rent_a_car_Naziv` ASC) VISIBLE,
  CONSTRAINT `fk_Auta_Rent_a_car1`
    FOREIGN KEY (`Rent_a_car_Naziv`)
    REFERENCES `mydb`.`rent_a_car` (`Naziv`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`kupci`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`kupci` (
  `idKupci` INT NOT NULL,
  `Ime` VARCHAR(45) NOT NULL,
  `Prezime` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Broj_telefona` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idKupci`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`iznajmljivanje`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`iznajmljivanje` (
  `Auta_Broj_sasije` CHAR(17) NOT NULL,
  `Auta_Rent_a_car_Naziv` VARCHAR(45) NOT NULL,
  `Kupci_idKupci` INT NOT NULL,
  `Datum_iznajmljivanja` DATE NOT NULL,
  `Datum_vracanja` DATE NOT NULL,
  PRIMARY KEY (`Auta_Broj_sasije`, `Auta_Rent_a_car_Naziv`, `Kupci_idKupci`),
  INDEX `fk_Iznajmljivanje_Kupci1_idx` (`Kupci_idKupci` ASC) VISIBLE,
  INDEX `fk_Iznajmljivanje_Auta1_idx` (`Auta_Rent_a_car_Naziv` ASC, `Auta_Broj_sasije` ASC) VISIBLE,
  CONSTRAINT `fk_Iznajmljivanje_Auta1`
    FOREIGN KEY (`Auta_Rent_a_car_Naziv` , `Auta_Broj_sasije`)
    REFERENCES `mydb`.`auta` (`Rent_a_car_Naziv` , `Broj_sasije`),
  CONSTRAINT `fk_Iznajmljivanje_Kupci1`
    FOREIGN KEY (`Kupci_idKupci`)
    REFERENCES `mydb`.`kupci` (`idKupci`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`rezervacija`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`rezervacija` (
  `Kupci_idKupci` INT NOT NULL,
  `Auta_Rent_a_car_Naziv` VARCHAR(45) NOT NULL,
  `Auta_Broj_sasije` CHAR(17) NOT NULL,
  `Dana` INT NOT NULL,
  PRIMARY KEY (`Kupci_idKupci`, `Auta_Rent_a_car_Naziv`, `Auta_Broj_sasije`),
  INDEX `fk_Rezervacija_Auta1_idx` (`Auta_Rent_a_car_Naziv` ASC, `Auta_Broj_sasije` ASC) VISIBLE,
  CONSTRAINT `fk_Rezervacija_Auta1`
    FOREIGN KEY (`Auta_Rent_a_car_Naziv` , `Auta_Broj_sasije`)
    REFERENCES `mydb`.`auta` (`Rent_a_car_Naziv` , `Broj_sasije`),
  CONSTRAINT `fk_Rezervacija_Kupci1`
    FOREIGN KEY (`Kupci_idKupci`)
    REFERENCES `mydb`.`kupci` (`idKupci`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
