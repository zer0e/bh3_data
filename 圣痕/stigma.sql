/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50151
Source Host           : localhost:3306
Source Database       : bh3

Target Server Type    : MYSQL
Target Server Version : 50151
File Encoding         : 65001

Date: 2020-03-19 16:40:52
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `stigma`
-- ----------------------------
DROP TABLE IF EXISTS `stigma`;
CREATE TABLE `stigma` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`stig_name`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`stig_class`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`stig_img`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`stig_hp`  int(11) NULL DEFAULT NULL ,
`stig_attack`  int(11) NULL DEFAULT NULL ,
`stig_def`  int(11) NULL DEFAULT NULL ,
`stig_huixin`  int(11) NULL DEFAULT NULL ,
`stig_skill`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1

;

-- ----------------------------
-- Auto increment value for `stigma`
-- ----------------------------
ALTER TABLE `stigma` AUTO_INCREMENT=1;
