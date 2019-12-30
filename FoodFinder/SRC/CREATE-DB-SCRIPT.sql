CREATE TABLE `Recipe` (
	`Id` SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(255) NOT NULL,
	`Prep_Time` TIME NOT NULL,
	`Calories` MEDIUMINT(8) UNSIGNED NULL DEFAULT NULL,
	`Url` VARCHAR(510) NOT NULL,
	`Image` VARCHAR(510) NULL DEFAULT NULL,
	PRIMARY KEY (`Id`),
	INDEX `IDX_Prep_Time` (`Prep_Time`),
	FULLTEXT INDEX `IDX_Name` (`Name`)
);

CREATE TABLE `Diet` (
	`Id` SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(255) NOT NULL,
	`Description` TEXT NULL,
	PRIMARY KEY (`Id`),
	INDEX `IDX_Name` (`Name`)
);

CREATE TABLE `Category` (
	`Id` SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(255) NOT NULL,
	`Description` TEXT NULL,
	PRIMARY KEY (`Id`),
	INDEX `IDX_Name` (`Name`)
);

CREATE TABLE `Ingredient` (
	`Id` SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(255) NOT NULL,
	`Category_Id` SMALLINT(5) UNSIGNED NOT NULL,
	PRIMARY KEY (`Id`),
	INDEX `IDX_Name` (`Name`),
	INDEX `FK_Ingredient_Category` (`Category_Id`),
	CONSTRAINT `FK_Ingredient_Category` FOREIGN KEY (`Category_Id`) REFERENCES `Category` (`id`) ON UPDATE CASCADE
);

CREATE TABLE `Recipe_Diet` (
	`Recipe_Id` SMALLINT(5) UNSIGNED NOT NULL,
	`Diet_Id` SMALLINT(5) UNSIGNED NOT NULL,
	PRIMARY KEY (`Recipe_Id`, `Diet_Id`),
	INDEX `FK_Recipe_Diet_Diet` (`Diet_Id`),
	CONSTRAINT `FK_Recipe_Diet_Diet` FOREIGN KEY (`Diet_Id`) REFERENCES `Diet` (`id`) ON UPDATE CASCADE,
	CONSTRAINT `FK_Recipe_Diet_Recipe` FOREIGN KEY (`Recipe_Id`) REFERENCES `Recipe` (`Id`) ON UPDATE CASCADE
);

CREATE TABLE `Recipe_Ingredient` (
	`Recipe_Id` SMALLINT(5) UNSIGNED NOT NULL,
	`Ingredient_Id` SMALLINT(5) UNSIGNED NOT NULL,
	`Weight` FLOAT UNSIGNED NULL DEFAULT NULL,
	`Description` TEXT NULL,
	PRIMARY KEY (`Recipe_Id`, `Ingredient_Id`),
	INDEX `FK_Recipe_Ingredient_Ingredient` (`Ingredient_Id`),
	CONSTRAINT `FK_Recipe_Ingredient_Ingredient` FOREIGN KEY (`Ingredient_Id`) REFERENCES `Ingredient` (`id`) ON UPDATE CASCADE,
	CONSTRAINT `FK_Recipe_Ingredient_Recipe` FOREIGN KEY (`Recipe_Id`) REFERENCES `Recipe` (`id`) ON UPDATE CASCADE
);
