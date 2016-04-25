-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'User'
-- 用户表
-- ---

DROP TABLE IF EXISTS `User`;
		
CREATE TABLE `User` (
  `id` INTEGER(50) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `sex` VARCHAR(10) NULL,
  `photo` VARCHAR(255) NULL,
  PRIMARY KEY (`id`)
) COMMENT '用户表';

-- ---
-- Table 'Blog'
-- 博客表
-- ---

DROP TABLE IF EXISTS `Blog`;
		
CREATE TABLE `Blog` (
  `id` INTEGER(50) NOT NULL AUTO_INCREMENT,
  `user_id` INTEGER(50) NOT NULL,
  `content` VARCHAR(255) NOT NULL,
  `fromBlog_id` INTEGER(50) NOT NULL,
  `fromUser_id` INTEGER(50) NOT NULL,
  `fowardNum` INTEGER(50) NOT NULL,
  `issueTime` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`)
) COMMENT '博客表';

-- ---
-- Table 'BlogImage'
-- 
-- ---

DROP TABLE IF EXISTS `BlogImage`;
		
CREATE TABLE `BlogImage` (
  `id` INTEGER(20) NOT NULL AUTO_INCREMENT,
  `blog_id` INTEGER(50) NOT NULL,
  `blog_image` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'Answer'
-- 回复表
-- ---

DROP TABLE IF EXISTS `Answer`;
		
CREATE TABLE `Answer` (
  `id` INTEGER(50) NOT NULL AUTO_INCREMENT,
  `fromUser_id` INTEGER(50) NOT NULL,
  `toUser_id` INTEGER(50) NOT NULL,
  `bolg_id` INTEGER(50) NOT NULL,
  `content` VARCHAR(50) NOT NULL,
  `resTime` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) COMMENT '回复表';

-- ---
-- Table 'UserFriend'
-- 
-- ---

DROP TABLE IF EXISTS `UserFriend`;
		
CREATE TABLE `UserFriend` (
  `id` INTEGER(50) NOT NULL AUTO_INCREMENT,
  `friend_id` INTEGER(50) NOT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `Blog` ADD FOREIGN KEY (user_id) REFERENCES `User` (`id`);
ALTER TABLE `BlogImage` ADD FOREIGN KEY (blog_id) REFERENCES `Blog` (`id`);
ALTER TABLE `Answer` ADD FOREIGN KEY (fromUser_id) REFERENCES `User` (`id`);
ALTER TABLE `Answer` ADD FOREIGN KEY (toUser_id) REFERENCES `User` (`id`);
ALTER TABLE `Answer` ADD FOREIGN KEY (bolg_id) REFERENCES `Blog` (`id`);
ALTER TABLE `UserFriend` ADD FOREIGN KEY (friend_id) REFERENCES `User` (`id`);


ALTER TABLE `Blog` ADD FOREIGN KEY (user_id) REFERENCES `User` (`id`);
ALTER TABLE `Blog` ADD FOREIGN KEY (fromUser_id) REFERENCES `User` (`id`);
ALTER TABLE `BlogImage` ADD FOREIGN KEY (blog_id) REFERENCES `Blog` (`id`);
ALTER TABLE `Answer` ADD FOREIGN KEY (fromUser_id) REFERENCES `User` (`id`);
ALTER TABLE `Answer` ADD FOREIGN KEY (toUser_id) REFERENCES `User` (`id`);
ALTER TABLE `Answer` ADD FOREIGN KEY (bolg_id) REFERENCES `Blog` (`id`);
ALTER TABLE `UserFriend` ADD FOREIGN KEY (friend_id) REFERENCES `User` (`id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `User` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Blog` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `BlogImage` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Answer` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `UserFriend` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `User` (`id`,`username`,`password`,`sex`,`photo`) VALUES
-- ('','','','','');
-- INSERT INTO `Blog` (`id`,`user_id`,`content`,`fromBlog_id`,`fromUser_id`,`fowardNum`,`issueTime`) VALUES
-- ('','','','','','','');
-- INSERT INTO `BlogImage` (`id`,`blog_id`,`blog_image`) VALUES
-- ('','','');
-- INSERT INTO `Answer` (`id`,`fromUser_id`,`toUser_id`,`bolg_id`,`content`,`resTime`) VALUES
-- ('','','','','','');
-- INSERT INTO `UserFriend` (`id`,`friend_id`) VALUES
-- ('','');