/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50151
Source Host           : localhost:3306
Source Database       : bh3

Target Server Type    : MYSQL
Target Server Version : 50151
File Encoding         : 65001

Date: 2020-03-19 16:41:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `weapon`
-- ----------------------------
DROP TABLE IF EXISTS `weapon`;
CREATE TABLE `weapon` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`weapon_name`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`weapon_img`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`weapon_intro`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`weapon_class`  int(11) NULL DEFAULT NULL COMMENT '1双枪 \r\n2太刀 \r\n3重炮 \r\n4大剑 \r\n5十字架 \r\n6拳套 \r\n7镰刀 \r\n8骑士枪 ' ,
`weapon_star`  int(11) NULL DEFAULT NULL ,
`weapon_attack`  int(11) NULL DEFAULT NULL ,
`weapon_huixin`  int(11) NULL DEFAULT NULL ,
`skill1`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`skill2`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`skill3`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1

;

-- ----------------------------
-- Auto increment value for `weapon`
-- ----------------------------
ALTER TABLE `weapon` AUTO_INCREMENT=1;
