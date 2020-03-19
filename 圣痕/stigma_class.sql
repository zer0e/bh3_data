/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50151
Source Host           : localhost:3306
Source Database       : bh3

Target Server Type    : MYSQL
Target Server Version : 50151
File Encoding         : 65001

Date: 2020-03-19 16:41:17
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `stigma_class`
-- ----------------------------
DROP TABLE IF EXISTS `stigma_class`;
CREATE TABLE `stigma_class` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`stig_class_name`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`get_function`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`stig_class_intro`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`stig_class_img1`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`stig_class_img2`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`stig_class_star`  int(11) NULL DEFAULT NULL ,
`two_stig_skill`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`three_stig_skill`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1

;

-- ----------------------------
-- Auto increment value for `stigma_class`
-- ----------------------------
ALTER TABLE `stigma_class` AUTO_INCREMENT=1;
