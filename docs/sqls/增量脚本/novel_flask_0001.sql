ALTER TABLE book ADD COLUMN comment_enabled tinyint(1) DEFAULT '1' COMMENT '是否允许评论，1是，0作家关闭评论区，2管理员关闭评论区，默认1' AFTER crawl_is_stop;

-- ----------------------------
-- Table structure for author_follow
-- ----------------------------
DROP TABLE IF EXISTS `author_follow`;
CREATE TABLE `author_follow` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `author_id` bigint DEFAULT NULL COMMENT '作家ID',
  `user_id` bigint DEFAULT NULL COMMENT '用户ID',
  `visit_count` int DEFAULT '0' COMMENT '访问次数',
  `create_time` datetime DEFAULT NULL COMMENT '关注事件',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_authorid_userid` (`author_id`,`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作家关注表';
