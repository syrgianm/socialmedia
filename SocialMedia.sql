-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema SocialMedia
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `SocialMedia` ;

-- -----------------------------------------------------
-- Schema SocialMedia
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `SocialMedia` DEFAULT CHARACTER SET utf8 ;
USE `SocialMedia` ;

-- -----------------------------------------------------
-- Table `SocialMedia`.`Profile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Profile` (
  `Username` VARCHAR(30) NOT NULL,
  `Password` VARCHAR(40) NOT NULL,
  `Email` VARCHAR(50) NOT NULL,
  `Phone` BIGINT(10) NOT NULL,
  `Street` VARCHAR(50) NULL,
  `City` VARCHAR(50) NULL,
  `Zip` INT NULL,
  `Private` TINYINT(1) NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC),
  UNIQUE INDEX `Phone_UNIQUE` (`Phone` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Post` (
  `PostID` INT NOT NULL,
  `Date_Time` DATETIME NULL,
  `Description` VARCHAR(200) NULL,
  `Username` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`PostID`),
  INDEX `Username_idx` (`Username` ASC),
  CONSTRAINT `Username`
    FOREIGN KEY (`Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Photo_Video_MultipleValue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Photo_Video_MultipleValue` (
  `Photo_Video` VARCHAR(100) NOT NULL,
  `PostID` INT NOT NULL,
  PRIMARY KEY (`Photo_Video`, `PostID`),
  INDEX `PostID_idx` (`PostID` ASC),
  CONSTRAINT `FK_PostID`
    FOREIGN KEY (`PostID`)
    REFERENCES `SocialMedia`.`Post` (`PostID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Comments` (
  `CommentID` INT NOT NULL,
  `PostID` INT NOT NULL,
  `Comment_Username` VARCHAR(30) NOT NULL,
  `Date_Time` DATETIME NULL,
  `Text` VARCHAR(200) NULL,
  `Photo_Video` VARCHAR(100) NULL,
  PRIMARY KEY (`CommentID`, `PostID`),
  INDEX `Comment-Username_idx` (`Comment_Username` ASC),
  INDEX `FK_PostID_idx` (`PostID` ASC),
  CONSTRAINT `FK_Comment_PostID`
    FOREIGN KEY (`PostID`)
    REFERENCES `SocialMedia`.`Post` (`PostID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Comment_Username`
    FOREIGN KEY (`Comment_Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Personal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Personal` (
  `Username` VARCHAR(30) NOT NULL,
  `DateOfBirth` DATE NULL,
  `Age` INT NULL,
  `Gender` ENUM('MALE', 'FEMALE') NULL,
  `Job` VARCHAR(50) NULL,
  `Status` ENUM("Free", "Married", "In-Relationship", "Widowed") NULL,
  `FirstName` VARCHAR(30) NULL,
  `LastName` VARCHAR(30) NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `FK_Pers_Username`
    FOREIGN KEY (`Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Page`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Page` (
  `Username` VARCHAR(30) NOT NULL,
  `Genre` ENUM("Entertainment", "Information", "Group", "Clothing", "Electrical") NULL,
  `Description` VARCHAR(200) NULL,
  `PageName` VARCHAR(30) CHARACTER SET 'big5' NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `FK_Page_Username`
    FOREIGN KEY (`Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Education_MultipleValue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Education_MultipleValue` (
  `Username` VARCHAR(30) NOT NULL,
  `Education` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`Username`, `Education`),
  CONSTRAINT `FK_Username`
    FOREIGN KEY (`Username`)
    REFERENCES `SocialMedia`.`Personal` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Friends` (
  `Username_1` VARCHAR(30) NOT NULL,
  `Username_2` VARCHAR(30) NOT NULL,
  `Date_Time` DATETIME NULL,
  PRIMARY KEY (`Username_1`, `Username_2`),
  INDEX `Username_2_idx` (`Username_2` ASC),
  CONSTRAINT `FK_Username_1`
    FOREIGN KEY (`Username_1`)
    REFERENCES `SocialMedia`.`Personal` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Username_2`
    FOREIGN KEY (`Username_2`)
    REFERENCES `SocialMedia`.`Personal` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Friend_Request`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Friend_Request` (
  `From_Username` VARCHAR(30) NOT NULL,
  `To_Username` VARCHAR(30) NOT NULL,
  `Date_Time` DATETIME NULL,
  PRIMARY KEY (`From_Username`, `To_Username`),
  INDEX `Username_2_idx` (`To_Username` ASC),
  CONSTRAINT `FK_From-Username`
    FOREIGN KEY (`From_Username`)
    REFERENCES `SocialMedia`.`Personal` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_To-Username`
    FOREIGN KEY (`To_Username`)
    REFERENCES `SocialMedia`.`Personal` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Follow`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Follow` (
  `Page_Username` VARCHAR(30) NOT NULL,
  `Pers_Username` VARCHAR(30) NOT NULL,
  `Date_Time` DATETIME NULL,
  PRIMARY KEY (`Page_Username`, `Pers_Username`),
  INDEX `Pers_Username_idx` (`Pers_Username` ASC),
  CONSTRAINT `FK_Page_Username_F`
    FOREIGN KEY (`Page_Username`)
    REFERENCES `SocialMedia`.`Page` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Pers_Username_F`
    FOREIGN KEY (`Pers_Username`)
    REFERENCES `SocialMedia`.`Personal` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Shares`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Shares` (
  `PostID` INT NOT NULL,
  `Share_Username` VARCHAR(30) NOT NULL,
  `Date_Time` DATETIME NULL,
  PRIMARY KEY (`PostID`, `Share_Username`),
  INDEX `Share-Username_idx` (`Share_Username` ASC),
  CONSTRAINT `FK_Shares_PostID`
    FOREIGN KEY (`PostID`)
    REFERENCES `SocialMedia`.`Post` (`PostID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Share_Username`
    FOREIGN KEY (`Share_Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Likes_Post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Likes_Post` (
  `PostID` INT NOT NULL,
  `Likes_Username` VARCHAR(30) NOT NULL,
  `Date_TIme` DATETIME NULL,
  PRIMARY KEY (`PostID`, `Likes_Username`),
  INDEX `Likes-Username_idx` (`Likes_Username` ASC),
  CONSTRAINT `FK_Likes_PostID`
    FOREIGN KEY (`PostID`)
    REFERENCES `SocialMedia`.`Post` (`PostID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Likes_Username`
    FOREIGN KEY (`Likes_Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Likes_Comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Likes_Comment` (
  `PostID` INT NOT NULL,
  `CommentID` INT NOT NULL,
  `Comment_Like_Username` VARCHAR(30) NOT NULL,
  `Date_Time` DATETIME NULL,
  PRIMARY KEY (`PostID`, `CommentID`, `Comment_Like_Username`),
  INDEX `CommentID_idx` (`CommentID` ASC),
  INDEX `Comment-Like-Username_idx` (`Comment_Like_Username` ASC))
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `SocialMedia`.`Send_Message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SocialMedia`.`Send_Message` (
  `Date_Time` DATETIME NULL,
  `Text` VARCHAR(200) NULL,
  `Photo_Video` VARCHAR(100) NULL,
  `Was_Read` TINYINT(1) NOT NULL,
  `From_Username` VARCHAR(30) NOT NULL,
  `To_Username` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`Date_Time`, `From_Username`, `To_Username`),
  INDEX `fk_Send Message_Profile1_idx` (`From_Username` ASC),
  INDEX `fk_Send Message_Profile2_idx` (`To_Username` ASC),
  CONSTRAINT `FK_From_Username`
    FOREIGN KEY (`From_Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_To_Username`
    FOREIGN KEY (`To_Username`)
    REFERENCES `SocialMedia`.`Profile` (`Username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `SocialMedia`;

DELIMITER $$
USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Profile_BEFORE_INSERT` BEFORE INSERT ON `Profile` FOR EACH ROW
BEGIN
	IF (new.Phone >= 6999999999) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'phone number is invalid';
	END IF;
    
    IF (new.Email NOT LIKE '%@%') THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'email is invalid';
	END IF;
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Post_BEFORE_INSERT` BEFORE INSERT ON `Post` FOR EACH ROW
BEGIN
	set new.Date_Time = now();
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Comments_BEFORE_INSERT` BEFORE INSERT ON `Comments` FOR EACH ROW
BEGIN
	set new.Date_Time = now();
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Personal_BEFORE_INSERT` BEFORE INSERT ON `Personal` FOR EACH ROW
BEGIN
	IF (new.Age <1 OR new.age >120) THEN
		signal sqlstate '45000' set message_text ='age is invalid';
	end if;
	IF (new.DateOfBirth not between '1900-1-1' AND '2021-12-12') then
		signal sqlstate '45000' set message_text = 'invalid date of birth';
	end if;
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Personal_BEFORE_UPDATE` BEFORE UPDATE ON `Personal` FOR EACH ROW
BEGIN
	IF (new.Age <1 OR new.age >120) THEN
		signal sqlstate '45000' set message_text ='age is invalid';
	end if;
	IF (new.DateOfBirth not between '1900-1-1' AND '2021-12-12') then
		signal sqlstate '45000' set message_text = 'invalid date of birth';
	end if;
END$$

USE `SocialMedia`$$
CREATE TRIGGER `SocialMedia`.`Friends_BEFORE_INSERT` 
BEFORE INSERT ON `Friends` FOR EACH ROW
BEGIN
	IF (new.Date_Time IS NULL) THEN
		set new.Date_Time = now();
	END IF;
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Friend_Request_BEFORE_INSERT` BEFORE INSERT ON `Friend_Request` FOR EACH ROW
BEGIN
	IF (new.Date_Time IS NULL) THEN
		set new.Date_Time = now();
	END IF;
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Follow_BEFORE_INSERT` BEFORE INSERT ON `Follow` FOR EACH ROW
BEGIN
	IF (new.Date_Time IS NULL) THEN
		set new.Date_Time = now();
	END IF;
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Shares_BEFORE_INSERT` BEFORE INSERT ON `Shares` FOR EACH ROW
BEGIN
	set new.Date_Time = now();
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Likes_Post_BEFORE_INSERT` BEFORE INSERT ON `Likes_Post` FOR EACH ROW
BEGIN
	IF (new.Date_Time IS NULL) THEN
		set new.Date_Time = now();
	END IF;
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Likes_Comment_BEFORE_INSERT` BEFORE INSERT ON `Likes_Comment` FOR EACH ROW
BEGIN
	IF (new.Date_Time IS NULL) THEN
		set new.Date_Time = now();
	END IF;
END$$

USE `SocialMedia`$$
CREATE DEFINER = CURRENT_USER TRIGGER `SocialMedia`.`Send_Message_BEFORE_INSERT` BEFORE INSERT ON `Send_Message` FOR EACH ROW
BEGIN
	set new.Date_Time = now();
END$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
