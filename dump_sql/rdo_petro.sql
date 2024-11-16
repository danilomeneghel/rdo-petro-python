-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema rdo_petro
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema rdo_petro
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `rdo_petro` ;
USE `rdo_petro` ;

-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_aprovador_contrada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_aprovador_contrada` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_aprovador_petrobras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_aprovador_petrobras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo_aprovador_contratada` INT NULL,
  `id_rdo_aprovador_petrobras` INT NULL,
  `nro_rdo` INT NULL,
  `data` DATE NULL,
  `ve` FLOAT NULL,
  `vm` FLOAT NULL,
  `delta` FLOAT NULL,
  `total_reducoes` FLOAT NULL,
  `tx_diaria` FLOAT NULL,
  `v_max` FLOAT NULL,
  `v_inj` FLOAT NULL,
  `v_cota` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_rdo_aprovador_contratada_idx` (`id_rdo_aprovador_contratada` ASC) VISIBLE,
  INDEX `fk_rdo_aprovador_petrobras_idx` (`id_rdo_aprovador_petrobras` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_aprovador_contratada`
    FOREIGN KEY (`id_rdo_aprovador_contratada`)
    REFERENCES `rdo_petro`.`rdo_aprovador_contrada` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rdo_aprovador_petrobras`
    FOREIGN KEY (`id_rdo_aprovador_petrobras`)
    REFERENCES `rdo_petro`.`rdo_aprovador_petrobras` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_gas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_gas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo` INT NULL,
  `gas_prod` FLOAT NULL,
  `gas_comb` FLOAT NULL,
  `gas_inj` FLOAT NULL,
  `gas_exp` FLOAT NULL,
  `gas_lp1` FLOAT NULL,
  `gas_lp2` FLOAT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_gas_idx` (`id_rdo` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_gas_rdo`
    FOREIGN KEY (`id_rdo`)
    REFERENCES `rdo_petro`.`rdo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_gas_queima`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_gas_queima` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo_gas` INT NULL,
  `queima_tot` FLOAT NULL,
  `queima_pb` FLOAT NULL,
  `queima_md` FLOAT NULL,
  `queima_piloto` FLOAT NULL,
  `queima_purga` FLOAT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_queima_idx` (`id_rdo_gas` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_queima_rdo_gas`
    FOREIGN KEY (`id_rdo_gas`)
    REFERENCES `rdo_petro`.`rdo_gas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_pob`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_pob` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo` INT NULL,
  `pob_tot` INT NULL,
  `pob_fixo` INT NULL,
  `pob_br` INT NULL,
  `pob_merg` INT NULL,
  `pob_pb` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_pob_idx` (`id_rdo` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_pob_rdo`
    FOREIGN KEY (`id_rdo`)
    REFERENCES `rdo_petro`.`rdo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_obs_contratada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_obs_contratada` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo` INT NULL,
  `item` VARCHAR(45) NULL,
  `referencia` VARCHAR(45) NULL,
  `contrato` VARCHAR(45) NULL,
  `descricao` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_comentario_idx` (`id_rdo` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_obs_contratada`
    FOREIGN KEY (`id_rdo`)
    REFERENCES `rdo_petro`.`rdo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'contrato\nENUM(AFRETAMENTO, SERVIÇO, AMBOS)';


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_obs_petrobras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_obs_petrobras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo` INT NULL,
  `item` VARCHAR(45) NULL,
  `referencia` VARCHAR(45) NULL,
  `contrato` VARCHAR(45) NULL,
  `descricao` VARCHAR(45) NULL,
  `tipo_coment` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_comentario_idx` (`id_rdo` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_obs_petrobras`
    FOREIGN KEY (`id_rdo`)
    REFERENCES `rdo_petro`.`rdo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'contrato\nENUM(AFRETAMENTO, SERVIÇO, AMBOS)';


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_obs_situacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_obs_situacao` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo_obs_petrobras` INT NULL,
  `status` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_obs_situacao_rdo_obs_petrobras_idx` (`id_rdo_obs_petrobras` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_obs_situacao_rdo_obs_petrobras`
    FOREIGN KEY (`id_rdo_obs_petrobras`)
    REFERENCES `rdo_petro`.`rdo_obs_petrobras` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'status\nENUM(CONCLUIDO, EM ANDAMENTO, PENDENTE, POSTERGADO, NÃO APLICAVEL)';


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_diesel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_diesel` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo` INT NULL,
  `diesel_pb` FLOAT NULL,
  `diesel_md` FLOAT NULL,
  `diesel_inicial` FLOAT NULL,
  `diesel_final` FLOAT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_diesel_rdo_idx` (`id_rdo` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_diesel_rdo`
    FOREIGN KEY (`id_rdo`)
    REFERENCES `rdo_petro`.`rdo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_contrato`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_contrato` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo` INT NULL,
  `nro_contrato` VARCHAR(45) NULL,
  `unid_producao` VARCHAR(45) NULL,
  `tipo_contrato` VARCHAR(45) NULL,
  `inicio_contrato` DATE NULL,
  `termino_contrato` DATE NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_contrato_rdo_idx` (`id_rdo` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_contrato_rdo`
    FOREIGN KEY (`id_rdo`)
    REFERENCES `rdo_petro`.`rdo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'tipo_contrato\nENUM(AFRETAMENTO, SERVIÇO, OUTRO)';


-- -----------------------------------------------------
-- Table `rdo_petro`.`rdo_reducao_tx_diaria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rdo_petro`.`rdo_reducao_tx_diaria` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_rdo` INT NULL,
  `tempo_ocorrencia` INT NULL,
  `tempo_extra` INT NULL,
  `perc_reducao` INT NULL,
  `item_anexo_a` VARCHAR(45) NULL,
  `contrato` VARCHAR(45) NULL,
  `hora_inicio` TIME NULL,
  `hora_fim` TIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rdo_reducao_tx_diaria_rdo_idx` (`id_rdo` ASC) VISIBLE,
  CONSTRAINT `fk_rdo_reducao_tx_diaria_rdo`
    FOREIGN KEY (`id_rdo`)
    REFERENCES `rdo_petro`.`rdo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'contrato\nENUM(AFRETAMENTO, SERVIÇO, AMBOS)\n';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
