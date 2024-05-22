SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for author
-- ----------------------------
DROP TABLE IF EXISTS `author`;
CREATE TABLE `author` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint DEFAULT NULL COMMENT '用户ID',
  `invite_code` varchar(20) DEFAULT NULL COMMENT '邀请码',
  `pen_name` varchar(20) DEFAULT NULL COMMENT '笔名',
  `tel_phone` varchar(20) DEFAULT NULL COMMENT '手机号码',
  `chat_account` varchar(50) DEFAULT NULL COMMENT 'QQ或微信账号',
  `email` varchar(50) DEFAULT NULL COMMENT '电子邮箱',
  `work_direction` tinyint DEFAULT NULL COMMENT '作品方向，0：男频，1：女频',
  `status` tinyint DEFAULT '0' COMMENT '0：正常，1：封禁',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作者表';

-- ----------------------------
-- Records of author
-- ----------------------------

-- ----------------------------
-- Table structure for author_code
-- ----------------------------
DROP TABLE IF EXISTS `author_code`;
CREATE TABLE `author_code` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `invite_code` varchar(100) DEFAULT NULL COMMENT '邀请码',
  `validity_time` datetime DEFAULT NULL COMMENT '有效时间',
  `is_use` tinyint(1) DEFAULT '0' COMMENT '是否使用过，0：未使用，1:使用过',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `create_user_id` bigint DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_code` (`invite_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作家邀请码表';

-- ----------------------------
-- Records of author_code
-- ----------------------------
INSERT INTO `author_code` VALUES ('3', 'reerer', '2020-05-27 22:43:45', '1', '2020-05-13 11:40:56', '1');
INSERT INTO `author_code` VALUES ('4', '123456', '2020-05-28 00:00:00', '0', '2020-05-13 14:09:55', '1');
INSERT INTO `author_code` VALUES ('5', 'ww34343', '2020-05-21 00:00:00', '0', '2020-05-13 14:18:58', '1');

-- ----------------------------
-- Table structure for author_income
-- ----------------------------
DROP TABLE IF EXISTS `author_income`;
CREATE TABLE `author_income` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `author_id` bigint NOT NULL COMMENT '作家ID',
  `book_id` bigint NOT NULL COMMENT '作品ID',
  `income_month` date NOT NULL COMMENT '收入月份',
  `pre_tax_income` bigint NOT NULL DEFAULT '0' COMMENT '税前收入（分）',
  `after_tax_income` bigint NOT NULL DEFAULT '0' COMMENT '税后收入（分）',
  `pay_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '支付状态，0：待支付，1：已支付',
  `confirm_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '稿费确认状态，0：待确认，1：已确认',
  `detail` varchar(255) DEFAULT NULL COMMENT '详情',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='稿费收入统计表';

-- ----------------------------
-- Records of author_income
-- ----------------------------

-- ----------------------------
-- Table structure for author_income_detail
-- ----------------------------
DROP TABLE IF EXISTS `author_income_detail`;
CREATE TABLE `author_income_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `author_id` bigint NOT NULL COMMENT '作家ID',
  `book_id` bigint NOT NULL DEFAULT '0' COMMENT '作品ID,0表示全部作品',
  `income_date` date NOT NULL COMMENT '收入日期',
  `income_account` int NOT NULL DEFAULT '0' COMMENT '订阅总额',
  `income_count` int NOT NULL DEFAULT '0' COMMENT '订阅次数',
  `income_number` int NOT NULL DEFAULT '0' COMMENT '订阅人数',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='稿费收入明细统计表';

-- ----------------------------
-- Records of author_income_detail
-- ----------------------------

-- ----------------------------
-- Table structure for book
-- ----------------------------
DROP TABLE IF EXISTS `book`;
CREATE TABLE `book` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `work_direction` tinyint(1) DEFAULT NULL COMMENT '作品方向，0：男频，1：女频''',
  `cat_id` int DEFAULT NULL COMMENT '分类ID',
  `cat_name` varchar(50) DEFAULT NULL COMMENT '分类名',
  `pic_url` varchar(200) NOT NULL COMMENT '小说封面',
  `book_name` varchar(50) NOT NULL COMMENT '小说名',
  `author_id` bigint DEFAULT NULL COMMENT '作者id',
  `author_name` varchar(50) NOT NULL COMMENT '作者名',
  `book_desc` varchar(2000) NOT NULL COMMENT '书籍描述',
  `score` float NOT NULL COMMENT '评分，预留字段',
  `book_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '书籍状态，0：连载中，1：已完结',
  `visit_count` bigint DEFAULT '103' COMMENT '点击量',
  `word_count` int DEFAULT NULL COMMENT '总字数',
  `comment_count` int DEFAULT '0' COMMENT '评论数',
  `yesterday_buy` int DEFAULT '0' COMMENT '昨日订阅数',
  `last_index_id` bigint DEFAULT NULL COMMENT '最新目录ID',
  `last_index_name` varchar(50) DEFAULT NULL COMMENT '最新目录名',
  `last_index_update_time` datetime DEFAULT NULL COMMENT '最新目录更新时间',
  `is_vip` tinyint(1) DEFAULT '0' COMMENT '是否收费，1：收费，0：免费',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态，0：入库，1：上架',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `crawl_source_id` int DEFAULT NULL COMMENT '爬虫源站ID',
  `crawl_book_id` varchar(32) DEFAULT NULL COMMENT '抓取的源站小说ID',
  `crawl_last_time` datetime DEFAULT NULL COMMENT '最后一次的抓取时间',
  `crawl_is_stop` tinyint(1) DEFAULT '0' COMMENT '是否已停止更新，0：未停止，1：已停止',
  `comment_enabled` tinyint(1) DEFAULT '1' COMMENT '是否允许评论，1是，0作家关闭评论区，2管理员关闭评论区，默认1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_bookName_authorName` (`book_name`,`author_name`) USING BTREE,
  KEY `key_lastIndexUpdateTime` (`last_index_update_time`) USING BTREE,
  KEY `key_createTime` (`create_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1262260513468559362 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说表';

-- ----------------------------
-- Records of book
-- ----------------------------

-- ----------------------------
-- Table structure for book_author
-- ----------------------------
DROP TABLE IF EXISTS `book_author`;
CREATE TABLE `book_author` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `invite_code` varchar(20) DEFAULT NULL COMMENT '邀请码',
  `pen_name` varchar(20) DEFAULT NULL COMMENT '笔名',
  `tel_phone` varchar(20) DEFAULT NULL COMMENT '手机号码',
  `chat_account` varchar(50) DEFAULT NULL COMMENT 'QQ或微信账号',
  `email` varchar(50) DEFAULT NULL COMMENT '电子邮箱',
  `work_direction` tinyint DEFAULT NULL COMMENT '作品方向，0：男频，1：女频',
  `status` tinyint DEFAULT NULL COMMENT '0：待审核，1：审核通过，正常，2：审核不通过',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `create_user_id` bigint DEFAULT NULL COMMENT '申请人ID',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `update_user_id` bigint DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1254957873655066625 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作者表';

-- ----------------------------
-- Records of book_author
-- ----------------------------

-- ----------------------------
-- Table structure for book_category
-- ----------------------------
DROP TABLE IF EXISTS `book_category`;
CREATE TABLE `book_category` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `work_direction` tinyint(1) DEFAULT NULL COMMENT '作品方向，0：男频，1：女频''',
  `name` varchar(20) NOT NULL COMMENT '分类名',
  `sort` tinyint NOT NULL DEFAULT '10' COMMENT '排序',
  `create_user_id` bigint DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_user_id` bigint DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说类别表';

-- ----------------------------
-- Records of book_category
-- ----------------------------
INSERT INTO `book_category` VALUES ('1', '0', '玄幻奇幻', '10', null, null, null, null);
INSERT INTO `book_category` VALUES ('2', '0', '武侠仙侠', '11', null, null, null, null);
INSERT INTO `book_category` VALUES ('3', '0', '都市言情', '12', null, null, null, null);
INSERT INTO `book_category` VALUES ('4', '0', '历史军事', '13', null, null, null, null);
INSERT INTO `book_category` VALUES ('5', '0', '科幻灵异', '14', null, null, null, null);
INSERT INTO `book_category` VALUES ('6', '0', '网游竞技', '15', null, null, null, null);
INSERT INTO `book_category` VALUES ('7', '1', '女生频道', '16', null, null, null, null);

-- ----------------------------
-- Table structure for book_comment
-- ----------------------------
DROP TABLE IF EXISTS `book_comment`;
CREATE TABLE `book_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `book_id` bigint DEFAULT NULL COMMENT '小说ID',
  `comment_content` varchar(512) DEFAULT NULL COMMENT '评价内容',
  `reply_count` int DEFAULT '0' COMMENT '回复数量',
  `audit_status` tinyint(1) DEFAULT '0' COMMENT '审核状态，0：待审核，1：审核通过，2：审核不通过',
  `create_time` datetime DEFAULT NULL COMMENT '评价时间',
  `create_user_id` bigint DEFAULT NULL COMMENT '评价人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_bookid_userid` (`book_id`,`create_user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说评论表';

-- ----------------------------
-- Records of book_comment
-- ----------------------------

-- ----------------------------
-- Table structure for book_comment_reply
-- ----------------------------
DROP TABLE IF EXISTS `book_comment_reply`;
CREATE TABLE `book_comment_reply` (
  `id` bigint NOT NULL COMMENT '主键',
  `comment_id` bigint DEFAULT NULL COMMENT '评论ID',
  `reply_content` varchar(512) DEFAULT NULL COMMENT '回复内容',
  `audit_status` tinyint(1) DEFAULT '0' COMMENT '审核状态，0：待审核，1：审核通过，2：审核不通过',
  `create_time` datetime DEFAULT NULL COMMENT '回复用户ID',
  `create_user_id` bigint DEFAULT NULL COMMENT '回复时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说评论回复表';

-- ----------------------------
-- Records of book_comment_reply
-- ----------------------------

-- ----------------------------
-- Table structure for book_content
-- ----------------------------
DROP TABLE IF EXISTS `book_content`;
CREATE TABLE `book_content` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3347665 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content
-- ----------------------------

-- ----------------------------
-- Table structure for book_content0
-- ----------------------------
DROP TABLE IF EXISTS `book_content0`;
CREATE TABLE `book_content0` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1155 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content0
-- ----------------------------

-- ----------------------------
-- Table structure for book_content1
-- ----------------------------
DROP TABLE IF EXISTS `book_content1`;
CREATE TABLE `book_content1` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=406 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content1
-- ----------------------------

-- ----------------------------
-- Table structure for book_content2
-- ----------------------------
DROP TABLE IF EXISTS `book_content2`;
CREATE TABLE `book_content2` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1222 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content2
-- ----------------------------

-- ----------------------------
-- Table structure for book_content3
-- ----------------------------
DROP TABLE IF EXISTS `book_content3`;
CREATE TABLE `book_content3` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=410 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content3
-- ----------------------------

-- ----------------------------
-- Table structure for book_content4
-- ----------------------------
DROP TABLE IF EXISTS `book_content4`;
CREATE TABLE `book_content4` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content4
-- ----------------------------

-- ----------------------------
-- Table structure for book_content5
-- ----------------------------
DROP TABLE IF EXISTS `book_content5`;
CREATE TABLE `book_content5` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=416 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content5
-- ----------------------------

-- ----------------------------
-- Table structure for book_content6
-- ----------------------------
DROP TABLE IF EXISTS `book_content6`;
CREATE TABLE `book_content6` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=859432137240084481 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content6
-- ----------------------------

-- ----------------------------
-- Table structure for book_content7
-- ----------------------------
DROP TABLE IF EXISTS `book_content7`;
CREATE TABLE `book_content7` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=404 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content7
-- ----------------------------

-- ----------------------------
-- Table structure for book_content8
-- ----------------------------
DROP TABLE IF EXISTS `book_content8`;
CREATE TABLE `book_content8` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=859432029832347649 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content8
-- ----------------------------

-- ----------------------------
-- Table structure for book_content9
-- ----------------------------
DROP TABLE IF EXISTS `book_content9`;
CREATE TABLE `book_content9` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_id` bigint DEFAULT NULL COMMENT '目录ID',
  `content` mediumtext COMMENT '小说章节内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_indexId` (`index_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=415 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说内容表';

-- ----------------------------
-- Records of book_content9
-- ----------------------------

-- ----------------------------
-- Table structure for book_index
-- ----------------------------
DROP TABLE IF EXISTS `book_index`;
CREATE TABLE `book_index` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `book_id` bigint NOT NULL COMMENT '小说ID',
  `index_num` int NOT NULL COMMENT '目录号',
  `index_name` varchar(100) DEFAULT NULL COMMENT '目录名',
  `word_count` int DEFAULT NULL COMMENT '字数',
  `is_vip` tinyint DEFAULT '0' COMMENT '是否收费，1：收费，0：免费',
  `book_price` int DEFAULT '0' COMMENT '章节费用（屋币）',
  `storage_type` varchar(10) NOT NULL DEFAULT 'db' COMMENT '存储方式',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_bookId_indexNum` (`book_id`,`index_num`) USING BTREE,
  KEY `key_bookId` (`book_id`) USING BTREE,
  KEY `key_indexNum` (`index_num`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1652552480577622017 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说目录表';

-- ----------------------------
-- Records of book_index
-- ----------------------------

-- ----------------------------
-- Table structure for book_screen_bullet
-- ----------------------------
DROP TABLE IF EXISTS `book_screen_bullet`;
CREATE TABLE `book_screen_bullet` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `content_id` bigint NOT NULL COMMENT '小说内容ID',
  `screen_bullet` varchar(512) NOT NULL COMMENT '小说弹幕内容',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `key_contentId` (`content_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小说弹幕表';

-- ----------------------------
-- Records of book_screen_bullet
-- ----------------------------

-- ----------------------------
-- Table structure for book_setting
-- ----------------------------
DROP TABLE IF EXISTS `book_setting`;
CREATE TABLE `book_setting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `book_id` bigint DEFAULT NULL COMMENT '小说ID',
  `sort` tinyint DEFAULT NULL COMMENT '排序号',
  `type` tinyint(1) DEFAULT NULL COMMENT '类型，0：轮播图，1：顶部小说栏设置，2：本周强推，3：热门推荐，4：精品推荐',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `create_user_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `update_user_id` bigint DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='首页小说设置表';

-- ----------------------------
-- Records of book_setting
-- ----------------------------

-- ----------------------------
-- Table structure for friend_link
-- ----------------------------
DROP TABLE IF EXISTS `friend_link`;
CREATE TABLE `friend_link` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `link_name` varchar(50) NOT NULL COMMENT '链接名',
  `link_url` varchar(100) NOT NULL COMMENT '链接url',
  `sort` tinyint NOT NULL DEFAULT '11' COMMENT '排序号',
  `is_open` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否开启，0：不开启，1：开启',
  `create_user_id` bigint DEFAULT NULL COMMENT '创建人id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_user_id` bigint DEFAULT NULL COMMENT '更新者用户id',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of friend_link
-- ----------------------------
INSERT INTO `friend_link` VALUES ('5', '小说精品屋', 'https://novel.xxyopen.com', '11', '1', null, null, null, null);

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cat_id` int DEFAULT NULL COMMENT '类别ID',
  `cat_name` varchar(50) DEFAULT NULL COMMENT '分类名',
  `source_name` varchar(50) DEFAULT NULL COMMENT '来源',
  `title` varchar(100) DEFAULT NULL COMMENT '标题',
  `content` text COMMENT '内容',
  `read_count` bigint NOT NULL DEFAULT '0' COMMENT '阅读量',
  `create_time` datetime DEFAULT NULL COMMENT '发布时间',
  `create_user_id` bigint DEFAULT NULL COMMENT '发布人ID',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `update_user_id` bigint DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='新闻表';

-- ----------------------------
-- Records of news
-- ----------------------------
INSERT INTO `news` VALUES ('1', '1', '行业', '未知', '阅文推“单本可选新合同”：授权分级、免费或付费自选', '阅文推“单本可选新合同”：授权分级、免费或付费自选', '0', '2020-04-27 15:42:21', null, '2020-04-27 15:42:26', null);
INSERT INTO `news` VALUES ('2', '3', '资讯', '全媒派公众号', 'AI小说悄然流行：人类特有的创作力，已经被AI复制？', 'AI小说悄然流行：人类特有的创作力，已经被AI复制？', '0', '2020-04-28 15:44:07', null, '2020-04-28 15:44:12', null);

-- ----------------------------
-- Table structure for news_category
-- ----------------------------
DROP TABLE IF EXISTS `news_category`;
CREATE TABLE `news_category` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(20) NOT NULL COMMENT '分类名',
  `sort` tinyint NOT NULL DEFAULT '10' COMMENT '排序',
  `create_user_id` bigint DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_user_id` bigint DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='新闻类别表';

-- ----------------------------
-- Records of news_category
-- ----------------------------
INSERT INTO `news_category` VALUES ('1', '行业', '10', null, null, null, null);
INSERT INTO `news_category` VALUES ('3', '资讯', '11', null, null, null, null);

-- ----------------------------
-- Table structure for order_pay
-- ----------------------------
DROP TABLE IF EXISTS `order_pay`;
CREATE TABLE `order_pay` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `out_trade_no` bigint NOT NULL COMMENT '商户订单号',
  `trade_no` varchar(64) DEFAULT NULL COMMENT '支付宝/微信交易号',
  `pay_channel` tinyint(1) NOT NULL DEFAULT '1' COMMENT '支付渠道，1：支付宝，2：微信',
  `total_amount` int NOT NULL COMMENT '交易金额(单位元)',
  `user_id` bigint NOT NULL COMMENT '支付用户ID',
  `pay_status` tinyint(1) DEFAULT '2' COMMENT '支付状态：0：支付失败，1：支付成功，2：待支付',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='充值订单';

-- ----------------------------
-- Records of order_pay
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(50) NOT NULL COMMENT '登录名',
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录密码',
  `nick_name` varchar(50) DEFAULT NULL COMMENT '昵称',
  `user_photo` varchar(100) DEFAULT NULL COMMENT '用户头像',
  `user_sex` tinyint(1) DEFAULT NULL COMMENT '用户性别，0：男，1：女',
  `account_balance` bigint NOT NULL DEFAULT '0' COMMENT '账户余额',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '用户状态，0：正常',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_username` (`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1652552608025743362 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1652552608025743362', '17816600001', 'pbkdf2:sha256:260000$ZB6c6GyP25H7VTeB$8c37d0fa710e5df4ebff72547377152d00fe9c6ee47c07987e412511922d53cf', '佳妮儿', null, '1', '75', '0', '2023-05-10 18:00:00', '2023-05-10 18:00:00');
INSERT INTO `user` VALUES ('1652552608025743366', '17816600002', 'pbkdf2:sha256:260000$V3s2dkzybSTe3G0S$b2c7875338b74d0207d461e4bf4bd719d060e9e778f0abec485e7e6c710c59da', '工贼', null, null, '0', '0', '2023-05-12 18:00:00', '2023-05-12 18:00:00');
INSERT INTO `user` VALUES ('1652552608025743367', '17816610001', 'pbkdf2:sha256:260000$sbVZ0OxMiPsNt9QZ$d09e843609cf03c6326dd941e99577eb53af79f0c3b6ceb308acfb3849d9f840', '王二麻子', null, null, '2', '0', '2023-06-07 18:00:00', '2023-06-07 18:00:00');
INSERT INTO `user` VALUES ('1652552608025743369', '17816610002', 'pbkdf2:sha256:260000$hJkR11s1eYPKjTKU$646ce7a0a7adeeed32114aee127630bac61a541b09cd4125994ca67560cdd94e', '韭菜', null, null, '5566416', '0', '2023-06-28 18:00:00', '2023-06-28 18:00:00');

-- ----------------------------
-- Table structure for user_bookshelf
-- ----------------------------
DROP TABLE IF EXISTS `user_bookshelf`;
CREATE TABLE `user_bookshelf` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `book_id` bigint NOT NULL COMMENT '小说ID',
  `pre_content_id` bigint DEFAULT NULL COMMENT '上一次阅读的章节内容表ID',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_userid_bookid` (`user_id`,`book_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户书架表';

-- ----------------------------
-- Records of user_bookshelf
-- ----------------------------

-- ----------------------------
-- Table structure for user_buy_record
-- ----------------------------
DROP TABLE IF EXISTS `user_buy_record`;
CREATE TABLE `user_buy_record` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `book_id` bigint DEFAULT NULL COMMENT '购买的小说ID',
  `book_name` varchar(50) DEFAULT NULL COMMENT '购买的小说名',
  `book_index_id` bigint DEFAULT NULL COMMENT '购买的章节ID',
  `book_index_name` varchar(100) DEFAULT NULL COMMENT '购买的章节名',
  `buy_amount` int DEFAULT NULL COMMENT '购买使用的屋币数量',
  `create_time` datetime DEFAULT NULL COMMENT '购买时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_userId_indexId` (`user_id`,`book_index_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户消费记录表';

-- ----------------------------
-- Records of user_buy_record
-- ----------------------------

-- ----------------------------
-- Table structure for user_feedback
-- ----------------------------
DROP TABLE IF EXISTS `user_feedback`;
CREATE TABLE `user_feedback` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint DEFAULT NULL COMMENT '用户id',
  `content` varchar(512) DEFAULT NULL COMMENT '反馈内容',
  `create_time` datetime DEFAULT NULL COMMENT '反馈时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user_feedback
-- ----------------------------

-- ----------------------------
-- Table structure for user_read_history
-- ----------------------------
DROP TABLE IF EXISTS `user_read_history`;
CREATE TABLE `user_read_history` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `book_id` bigint NOT NULL COMMENT '小说ID',
  `pre_content_id` bigint DEFAULT NULL COMMENT '上一次阅读的章节内容表ID',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_uq_userid_bookid` (`user_id`,`book_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户阅读记录表';

-- ----------------------------
-- Records of user_read_history
-- ----------------------------

-- ----------------------------
-- Table structure for website_info
-- ----------------------------
DROP TABLE IF EXISTS `website_info`;
CREATE TABLE `website_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '网站名',
  `domain` varchar(50) NOT NULL COMMENT '网站域名',
  `keyword` varchar(50) NOT NULL COMMENT 'SEO关键词',
  `description` varchar(512) NOT NULL COMMENT '网站描述',
  `qq` varchar(20) NOT NULL COMMENT '站长QQ',
  `logo` varchar(200) NOT NULL COMMENT '网站logo图片（默认）',
  `logo_dark` varchar(200) NOT NULL COMMENT '网站logo图片（深色）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `create_user_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `update_user_id` bigint DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='网站信息表';

-- ----------------------------
-- Records of website_info
-- ----------------------------
INSERT INTO `website_info` VALUES ('1', '小说精品屋', 'www.xxyopen.com', '小说精品屋,小说,小说CMS,原创文学系统,开源小说系统,免费小说建站程序', '小说精品屋是一个多端（PC、WAP）阅读、功能完善的原创文学CMS系统，由前台门户系统、作家后台管理系统、平台后台管理系统、爬虫管理系统等多个子系统构成，支持会员充值、订阅模式、新闻发布和实时统计报表等功能，新书自动入库，老书自动更新。', '1179705413', 'https://youdoc.gitee.io/resource/images/logo/logo.png', 'https://youdoc.gitee.io/resource/images/logo/logo_white.png', null, null, null, null);

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
